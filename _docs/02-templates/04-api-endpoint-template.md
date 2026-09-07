# API Endpoint Design Template

> This is the team's own `API_Design_Template.md`, adopted unchanged as the canonical format for every file under `specs/{module}/api-design/`. Its response envelope (`result`/`isSuccess`/`statusCode`/`message`) is the **binding contract** for the whole backend — see `01-conventions/05-backend-conventions.md` §3 and Decision D-002.
>
> **File naming**: `specs/{module}/api-design/{NN}-{METHOD}-{resource}-{action}.md`, e.g. `specs/devices/api-design/01-post-devices-register.md`.

---

[TOC]

---
## Overview

[One or two sentences: what this endpoint does and which role(s) call it.]

## API Specification

| API        | URL             |
| ---------- | --------------- |
| POST       | /api/auth/login |
| Permission | N/A             |

## Request sample
```json
{
    "userName": "userName",
    "password": "password"
}
```

| Field    | Description                         | Data Type | Examples   |
| -------- | ----------------------------------- | --------- | ---------- |
| userName | The user name account need to login | string    | `userName` |
| password | The password of user name account   | string    | `password` |

## Response sample

```json
{
  "result": {
    "accessToken": "",
    "refreshToken": ""
  },
  "isSuccess": true,
  "statusCode": 200,
  "message": "Sign in successfully"
}
```

## Validation

<table>
    <th>Status code</th>
    <th>Description</th>
    <th>Examples</th>
    <tbody>
        <tr>
            <td>400</td>
            <td>The user name is missing</td>
<td>

```json
{
  "result": null,
  "isSuccess": false,
  "statusCode": 400,
  "message": "userName is missing."
}
```
</td>
        </tr>
        <tr>
            <td>400</td>
            <td>The password is missing</td>
<td>

```json
{
  "result": null,
  "isSuccess": false,
  "statusCode": 400,
  "message": "password is missing."
}
```
</td>
        </tr>
                <tr>
            <td>400</td>
            <td>The incorrect user name or password</td>
<td>

```json
{
  "result": null,
  "isSuccess": false,
  "statusCode": 400,
  "message": "Incorrect username or password. Try again."
}
```
</td>
        </tr>
    </tbody>
</table>

## Activity Diagram

```plantuml
@startuml
start
:User input username and password;
:User click the Login button;
if (Fail validation) then
  :Show the error message;
  :Login fail;
else
  :Return the results;
  :Login successfully;
endif
stop
@enduml
```

## Sequence Diagram

```plantuml
@startuml
actor User as user
participant Controller as controller
participant LoginService as service
participant Database as db

user -> controller: Call Login API
controller -> service: Handle the request
service -> service: Validate the request
alt If wrong validation
  service --> controller: Return error message.
  controller --> user: Display error message.
end
service -> service: Generate Login Token.
service -> db: Save Token and set Expire Time.
db --> service: Return results.
service --> controller: Return result.
controller --> user: Login successfully.
@enduml
```

---

## Notes for reuse on TrekLink endpoints

- Swap `plantuml` diagrams for `mermaid` if your renderer doesn't support PlantUML (both are fine — GitHub renders Mermaid natively in `.md` files, which PlantUML needs a plugin for).
- `Permission` row: use the role(s) allowed, e.g. `Admin, Staff` or `N/A` for public endpoints like login.
- For idempotent gateway-sync endpoints, add a row noting the idempotency key, e.g. `Idempotency-Key: eventId (path: deviceId:sessionId:sequenceNumber)`.
- Every 4xx/5xx branch documented here must have a matching integration test — see `02-templates/03-tasks-template.md` Phase 4.3.
