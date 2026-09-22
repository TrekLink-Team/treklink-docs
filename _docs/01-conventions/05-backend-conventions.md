# Backend Code & REST API Conventions (NestJS)

> **Contractual Consistency**: every endpoint, validation rule, error response, and transaction must conform to one predictable standard, the one already established in `API_Design_Template.md`, not a generic REST convention imported from elsewhere.

---

## 1. The Standard Module Structure

Every feature within a module (`src/modules/{module}/`) follows the same file set, no separate Command/Query folders; NestJS services are already a natural CQRS-lite (a service method is a command or a query, distinguished by whether it mutates):

```text
modules/devices/
├── devices.module.ts
├── devices.controller.ts       # thin — maps HTTP to service calls
├── devices.service.ts          # business rules, FSM, transactions
├── dto/
│   ├── create-device.dto.ts    # class-validator decorated request shape
│   ├── update-device-status.dto.ts
│   └── device-response.dto.ts  # what goes inside `result`
├── entities/ (or a schema.prisma slice)
│   └── device.entity.ts
├── device-fsm.ts                # transition table (see 04-architecture-conventions.md §2.1)
└── devices.service.spec.ts / devices.controller.spec.ts
```

### 1.1 Service Method Invariants
- **Mutating methods** (`create`, `updateStatus`, `retire`, …): return the minimal DTO needed by the caller, never the raw ORM entity, never an over-fetched aggregate.
- **Read methods** (`findAll`, `findById`, …): never mutate, never trigger side effects (no notification dispatch from inside a `findById`).

---

## 2. Input Validation

Validation runs **before** the controller method body executes, via NestJS's global `ValidationPipe` + `class-validator` decorators on the DTO, this is the direct equivalent of a "pipeline behavior," no extra library needed.

```typescript
export class CreateDeviceDto {
  @IsString() @IsNotEmpty()
  hardwareVariant: string;

  @IsEnum(DeviceStatus) @IsOptional()
  status?: DeviceStatus;
}
```

### Golden Rules
1. **Zero hardcoded error strings in controllers/services.** Centralize error codes in `common/error-codes.enum.ts` (e.g. `DEVICE_NOT_FOUND`, `INVALID_STATE_TRANSITION`, `DUPLICATE_EVENT_ID`).
2. **Field-scoped errors**: `class-validator`'s default output already includes the offending property, pass it through in the `message`, don't flatten it away.

---

## 3. The Canonical Response Envelope (binding: from `API_Design_Template.md`)

This supersedes any other backend framework's default response shape. **Every** endpoint, success or failure, returns this exact shape:

```json
{
  "result": { "...": "..." },
  "isSuccess": true,
  "statusCode": 200,
  "message": "Sign in successfully"
}
```

Failure example:
```json
{
  "result": null,
  "isSuccess": false,
  "statusCode": 400,
  "message": "userName is missing."
}
```

### 3.1 Implementation: Global Interceptor + Exception Filter

```typescript
// common/interceptors/response.interceptor.ts
@Injectable()
export class ResponseInterceptor implements NestInterceptor {
  intercept(ctx: ExecutionContext, next: CallHandler) {
    const res = ctx.switchToHttp().getResponse();
    return next.handle().pipe(
      map((result) => ({
        result: result ?? null,
        isSuccess: true,
        statusCode: res.statusCode,
        message: 'Success',
      })),
    );
  }
}

// common/filters/http-exception.filter.ts
@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const res = host.switchToHttp().getResponse();
    const status = exception instanceof HttpException ? exception.getStatus() : 500;
    const message = exception instanceof HttpException
      ? (exception.getResponse() as any).message ?? exception.message
      : 'Internal server error';
    res.status(status).json({ result: null, isSuccess: false, statusCode: status, message });
  }
}
```

Register both globally in `main.ts` so no controller ever hand-rolls a response shape.

### 3.2 Paged Collections
Nest the standard `PagedResultDto` **inside** `result`:
```json
{
  "result": {
    "items": [ "..." ],
    "pageNumber": 1,
    "pageSize": 20,
    "totalCount": 142,
    "totalPages": 8
  },
  "isSuccess": true,
  "statusCode": 200,
  "message": "Success"
}
```

---

## 4. Status Code & Error Taxonomy

| HTTP Status | When |
|---|---|
| `200 OK` | Successful read or mutation with a body |
| `201 Created` | Resource created, still uses the same envelope (not a bare Location header pattern) |
| `400 Bad Request` | DTO validation failure |
| `401 Unauthorized` | Missing/expired JWT |
| `403 Forbidden` | Valid JWT, insufficient role/CASL policy |
| `404 Not Found` | Resource doesn't exist |
| `409 Conflict` | State-transition violation (e.g. renting an already-`Rented` device), duplicate unique field |
| `500 Internal Server Error` | Unhandled, logged with a trace ID, generic message returned to client |

Controllers **never** contain `try/catch` for expected errors, throw NestJS `HttpException` subclasses (`BadRequestException`, `ConflictException`, …) and let `GlobalExceptionFilter` shape the response.

---

## 5. Controller Standards

```typescript
@Controller('api/devices')
export class DevicesController {
  constructor(private readonly devicesService: DevicesService) {}

  @Post()
  @UseGuards(JwtAuthGuard, PoliciesGuard)
  @CheckPolicies((ability) => ability.can('create', 'Device'))
  @ApiResponse({ status: 201, type: DeviceResponseDto })
  async create(@Body() dto: CreateDeviceDto) {
    return this.devicesService.create(dto);
  }
}
```
Three steps only: map input to a DTO, call the service, return the DTO (the interceptor wraps it). No business logic in controllers.

---

## 6. Async, Transactional & Concurrency Standards

1. **Async everywhere**: all DB/MQTT/HTTP I/O is `async`/`await`.
2. **Atomic units of work** for multi-table writes:
```typescript
await this.dataSource.transaction(async (manager) => {
  await manager.save(Rental, rental);
  await manager.update(Device, deviceId, { status: DeviceStatus.RENTED });
});
// (Prisma equivalent: prisma.$transaction([...]))
```
3. **Concurrency control**: the gateway-sync idempotency check + Incident creation MUST happen inside one transaction (see `04-architecture-conventions.md` §3), this is exactly what the register's concurrent-event NFR (20 simultaneous submissions, 0 duplicates) verifies. Use a DB-level unique constraint on `eventId` as the last line of defense, not just an application-level check.
