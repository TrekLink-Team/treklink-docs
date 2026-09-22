# TrekLink: Firmware Ground Truth

> **What this is**: verified facts about what `treklink-firmware` *actually does on the wire*, established by direct source inspection in Session 3 (extended Session 4). Every row cites `file:line`. Nothing here is inferred from the charter, the register, or Meshtastic upstream documentation.
>
> **Why it exists**: three separate specification assumptions turned out to contradict the firmware. Each cost a session to discover. This file is the reference that stops the fourth.
>
> **Status of the firmware repo**: **editable**, see **D-008**. Earlier docs describe it as frozen/read-only; that framing is superseded. Firmware *redesign* remains out of scope per charter §2.

---

## 1. The three assumptions that were wrong

| Assumed | Actual | Consequence |
|---|---|---|
| SOS has a distinct custom PortNum | **No custom PortNum exists.** SOS rides stock `TEXT_MESSAGE_APP` (1) and `POSITION_APP` (3), discriminated by an ASCII prefix on the text body | Gateway parser is coupled to a `printf` format string → **D-007** |
| `eventId = deviceId:sessionId:sequenceNumber` | **Neither `sessionId` nor `sequenceNumber` exists.** `MeshPacket.id` is a rolling-counter/random hybrid, re-seeded at boot | Idempotency key redefined → **D-006** |
| One SOS = one event | **One SOS = two independent packets** (position, then text), each with its own packet id | Backend must correlate; no single-frame dispatch → `gateway-sync/design.md` §2.4 |

---

## 2. SOS and fall detection

**Trigger path.** `TrekLinkSOSHelper::triggerSOS()` (`src/modules/TrekLinkSOSHelper.cpp:41–48`) executes in order:

1. `sendPositionPacket()` → `POSITION_APP`, `priority = MAX`, `want_ack = false`, `channel = 0` (`:118–121`)
2. `sendSOSTextMessage("SOS")` → `TEXT_MESSAGE_APP`, same flags (`:157–160`)
3. `activateAlarms()` → local buzzer/vibrator/LED only, no transmission

Callers: `TrekLinkButtonModule` (v1/v2 dedicated SOS button), `TrekLinkSOSGesture` (v3/v4, 3-second hold), `FallDetectionModule` (auto-SOS after pre-alarm timeout, `FallDetectionModule.cpp:145`, prefix `"SOS - FALL DETECTED"`).

**Wire formats.** `snprintf` templates at `TrekLinkSOSHelper.cpp:146` and `:148`, 100-byte buffer, truncated on overflow:

| Form | Emitted when |
|---|---|
| `SOS - [11.123456], [107.654321]` | button/gesture trigger, valid GPS fix |
| `SOS - [No GPS]` | button/gesture trigger, no valid fix |
| `SOS - FALL DETECTED - [11.123456], [107.654321]` | fall auto-SOS, valid fix |
| `SOS - FALL DETECTED - [No GPS]` | fall auto-SOS, no fix |

Parsers must test the fall prefix **first**, `"SOS - FALL DETECTED - …"` also satisfies `"SOS - "`.

**Beacon cadence.** `tickBeacon()` (`:181`): 5s intervals for the first 60s, then 30s, indefinitely until cancelled or the battery dies.

> ⚠️ **Beacons carry position only.** `tickBeacon` calls `broadcastPosition()`, never `sendSOSTextMessage()`. The text frame that *identifies* the episode as an SOS is transmitted **exactly once**, with `want_ack = false`. Lose it to RF and every subsequent packet looks like routine position reporting. Tracked as the **Critical** row in the risk register; firmware fix candidate #1 under D-008.

> ⚠️ **(Session 4) Beacons are also *not* high-priority.** `broadcastPosition()` calls `positionModule->sendOurPosition()` (`TrekLinkSOSHelper.cpp:61`), the module's ordinary periodic-broadcast path, **not** the manually-built packet `sendPositionPacket()` uses at trigger time. `PositionModule::sendOurPosition(NodeNum, bool, uint8_t)` (`PositionModule.cpp:377–380`) sets `p->priority` to `RELIABLE` only for `TRACKER`/`TAK_TRACKER` device roles, and **`BACKGROUND`**, the lowest tier, for every other role, which is what a handheld TrekLink unit is. So only the *first* position packet sent by `triggerSOS()` (built via `sendPositionPacket()`, `priority = MAX`, `:118–119`) is actually high-priority. Every beacon retransmit for the rest of the episode, 5s then 30s, "indefinitely", goes out at `BACKGROUND`, the same tier as routine chatter. Under mesh congestion, an ongoing emergency's beacon trail is currently the *least* protected traffic on the network after its opening packet. This also means D-007's "deferred precision upgrade" (switch to the `/2/e/` protobuf topic to recover `MeshPacket.priority`) would recover a `BACKGROUND` value for beacons, not a `MAX` one, there is no elevated priority left to recover past the first packet. New firmware-fix candidate, see D-008.
>
> `sendOurPosition()` also cancels any not-yet-transmitted prior position packet from the same node (`service->cancelSending(prevPacketId)`, `PositionModule.cpp:359–360`), each new beacon supersedes the last one still queued. Likely intentional (only the freshest position matters) but worth knowing when reasoning about "why didn't beacon N arrive" during dense mesh contention.

**Cancellation.** `cancelSOS()` (`:57–61`) calls only `deactivateAlarms()`. **No packet is transmitted on cancel**, the mesh and the backend are never told the episode ended. Open question: whether an episode can therefore only ever be closed by an operator.

> **(Session 4) Two visually-identical gestures, two very different effects.** Both `TrekLinkButtonModule` (v1/v2, dedicated SOS button) and `TrekLinkSOSGesture` (v3/v4, 3s hold on the general button, enforced at compile time by `TrekLinkVariantValidation.h`) support a hold-to-cancel action. It only has real effect during `FallDetectionModule`'s 30-second `PRE_ALARM` countdown (`FallDetectionModule.h: PREALARM_TIMEOUT = 30000`), i.e. *before* `triggerSOS()` has fired, when cancelling genuinely suppresses a false-positive fall detection and nothing is ever transmitted. Once `triggerSOS()` has fired (button/gesture SOS, or a confirmed fall past the pre-alarm window), the identical 3s-hold-and-release gesture calls `cancelSOS()`, which, per above, only silences local alarms. The backend has already received the broadcast; nothing retracts it. Guide-facing training material and UI copy should make this distinction explicit, since the physical action looks the same in both cases but means "false alarm, nothing was ever sent" in one and "I'm silencing my buzzer, the platform still thinks this is open" in the other.

**Dead constants.** `TREKLINK_MSG_SOS 0x01` and `TREKLINK_MSG_FALL 0x02` are `#define`d in three headers (`TrekLinkSOSHelper.h:23–27`, `TrekLinkButtonModule.h:43–44`, `FallDetectionModule.h:13–14`) and **referenced nowhere in the codebase**. They are not wire discriminators. Do not build a parser expecting them.

---

## 3. Packet identity

`generatePacketId()` (`src/mesh/Router.cpp:168–187`):

```c
rollingPacketId = random(...)          // re-seeded at every boot
rollingPacketId++
rollingPacketId &= ID_COUNTER_MASK     // keeps low 10 bits
id = rollingPacketId | random(...) << 10   // 22 random high bits
```

- **Not monotonic** across reboots, and not monotonic in the high bits at all.
- The 10-bit counter portion wraps every 1024 packets.
- Meshtastic's own purpose for this field is flood-dedup inside the mesh, not application sequencing.
- Assigned in `Router::allocForSending()` (`:198`), so every packet gets one.
- **(Session 4, checked and ruled out)** The protobuf field comment on `MeshPacket.id` claims IDs are "always 0 for no-ack or non-broadcast packets" (`mesh.pb.h:913–921`). Verified against `Router::allocForSending()` (`Router.cpp:198`): it unconditionally calls `generatePacketId()` for every packet regardless of `want_ack`/broadcast status. Every TrekLink SOS/position/telemetry packet gets a real, non-zero `packetId`, D-006's `sha256(nodeNum:packetId)` key is safe from this angle.

Also set there: `from = nodeDB->getNodeNum()`, `to = NODENUM_BROADCAST`, `rx_time = getValidTime(...)`, **which yields `0` when the device RTC holds no valid time.** Treat `rx_time == 0` as null, never as an epoch timestamp.

**(Session 4) `nodeNum` stability, answers `specs/gateway-sync/requirements.md` §5 Q8.** `pickNewNodeNum()` (`NodeDB.cpp:1123–1142`) derives a candidate from the device's MAC address (`ourMacAddr[2..5]`, `:1127`) and only picks a different candidate if that value collides with a *different* MAC already known in the local NodeDB (`:1131–1138`). So `nodeNum` is MAC-derived and stable for a given physical unit across ordinary reboots, good news for `Device.nodeNum @unique` fleet-registration stories, which assume a durable per-unit identifier. It is not a literal cryptographic guarantee (the collision-avoidance fallback means it is "MAC-derived, uniqueness-adjusted against locally-known peers," not a pure deterministic function of the MAC alone), so treat as reliable-in-practice rather than mathematically invariant.

---

## 4. MQTT uplink

**Topic structure** (`src/mqtt/MQTT.cpp:423–430`, `:798`), `<root>` is configurable, the rest is hardcoded:

```
<root>/2/e/<channelId>/<nodeId>      → ServiceEnvelope protobuf
<root>/2/json/<channelId>/<nodeId>   → JSON, when json_enabled
<root>/2/map/                        → MapReport, when map_reporting_enabled
```

Default `<root>` is `msh`. `ServiceEnvelope` carries `{ packet, channel_id, gateway_id }` (`mqtt.pb.h:16–25`).

**Config surface** (`module_config.pb.h:126–160`): `enabled`, `address[64]`, `username[64]`, `password[32]`, `encryption_enabled`, `json_enabled`, `root`, `proxy_to_client_enabled`, `map_reporting_enabled`.

**JSON envelope fields** (`src/serialization/MeshPacketSerializer.cpp:410–424`):
`id`, `timestamp`, `to`, `from`, `channel`, `type`, `sender`, `payload`, plus `rssi` / `snr` / `hops_away` / `hop_start` when non-zero.

> ⚠️ **`MeshPacket.priority` is absent from the JSON envelope.** The SOS position packet is sent at `priority = MAX` but arrives on the JSON topic indistinguishable from a routine position report. The `/2/e/` protobuf topic preserves it. See D-007.

**JSON PortNum coverage** (`MeshPacketSerializer.cpp`): `TEXT_MESSAGE_APP` (:28), `TELEMETRY_APP` (:56), `NODEINFO_APP` (:190), `POSITION_APP` (:208), `WAYPOINT_APP` (:253), `NEIGHBORINFO_APP` (:273), `TRACEROUTE_APP` (:299), `DETECTION_SENSOR_APP` (:353), `PAXCOUNTER_APP` (:363), `REMOTE_HARDWARE_APP` (:380). The three TrekLink actually emits are all covered.

> **(Session 4) `TELEMETRY_APP` is a protobuf `oneof`, not one payload shape.** `meshtastic_Telemetry` (`telemetry.pb.h:408–428`) carries a `which_variant` discriminator over `device_metrics` (`battery_level`, `voltage`, `channel_utilization`, `air_util_tx`, `uptime_seconds`), `environment_metrics` (`temperature`, `humidity`, ...), and others, but the JSON serialization (`MeshPacketSerializer.cpp:56–120`) does **not** emit an explicit variant-type key; a consumer must infer the variant from which fields are present. Both variants independently define a `voltage` field, so "has a `voltage` key" alone doesn't disambiguate them. Low real-world risk, TrekLink units almost certainly never emit `EnvironmentMetrics` (no such sensor module in `src/modules/`), but `TelemetryStrategy` (gateway-sync design §2.2) should guard on `battery_level`/`uptime_seconds` presence rather than assume every telemetry payload is device metrics, and the Phase 0.4 golden-fixture capture should include a device-metrics sample explicitly so the assumption is tested, not just believed.

`encryption_enabled = false` makes the broker receive decrypted packets, the field's own comment notes this exists for external consumers. The alternative is reimplementing Meshtastic's AES-CTR channel crypto in NestJS.

### 4.1 (Session 7) The node-side MQTT queue already exists: and discards SOS first

**A queue is already in the firmware.** It is stock Meshtastic, not TrekLink code, and it is emphatically *not* an offline store-and-forward buffer. Every property below is read from source, not inferred.

| Property | Verified value | Evidence |
|---|---|---|
| Depth | **16 entries, fixed at compile time** | `MQTT.h:27`, `#define MAX_MQTT_QUEUE 16` |
| Element | `{ std::string topic; std::basic_string<uint8_t> envBytes; }`, a pre-encoded `ServiceEnvelope` | `MQTT.h:68–72` |
| Storage | `PointerQueue<QueueEntry>` → `TypedQueue` → a FreeRTOS queue of heap pointers. **RAM.** | `MQTT.h:72`, `PointerQueue.h:8` |
| Survives reboot | **No.** No flash path exists on this code path at all. | absence of `FSCom`/`SafeFile` in `src/mqtt/` |
| Overflow policy | **Discards the OLDEST entry** and reuses its slot | `MQTT.cpp:821–823`, `LOG_WARN("MQTT queue is full, discard oldest"); entry = mqttQueue.dequeuePtr(0);` |
| Priority awareness | **None.** Strict FIFO; `MeshPacket.priority` is never consulted on enqueue. | `MQTT.cpp:818–831` |
| Drain rate | **One message per `runOnce()`**, which returns a 200 ms interval while draining | `MQTT.cpp:699–709`, `:607`, `:619` |
| Enqueue condition | only when `!proxy_to_client_enabled && !isConnectedDirectly()` | `MQTT.cpp:800`, `:818` |
| Reconnect period | 30 s while the link is wanted and down; 5 s when not wanted | `MQTT.cpp:621`, `:613` |

**Three consequences, in order of severity.**

1. ⚠️ **Drop-oldest + FIFO means an SOS is evicted by routine telemetry.** During an uplink outage the SOS beacon trail (5 s for the first 60 s, then 30 s, §2) plus ordinary telemetry fills all 16 slots in roughly **80 seconds**. Because eviction takes the *oldest* entry, the single `"SOS - …"` text frame that identifies the episode, transmitted exactly once, `want_ack = false` (§2), is **the first thing discarded**. This is the exact inverse of MF-02's binding rule that all `P0` events flush before any `P2`/`P3`.
2. **RAM-only storage makes exception scenario E02-3 unsatisfiable by construction.** A node reboot with a non-empty queue loses every buffered event.
3. **The discard is silent.** Nothing is published, counted, or surfaced; the eviction exists only as a `LOG_WARN` on a serial console nobody is reading in the field. RQ1's device-side loss denominator is therefore unobservable today.

**There is already a flash-persistence precedent in this repo to build on.** `MessageStore` (`src/MessageStore.cpp`, `src/MessageStore.h`) is a bounded, record-oriented, flash-backed queue: `MESSAGE_HISTORY_LIMIT 20` overridable from `build_flags` (`MessageStore.h:22–24`), fixed-size records serialized by `writeMessageRecord()` (`:244`), written through `SafeFile` onto `FSCom` (LittleFS on ESP32, `FSCommon.h:28`), with `saveToFlash()` called on shutdown from `Power.cpp:810` and from `MenuHandler.cpp:2142`, and `loadFromFlash()` at boot from `Screen.cpp:701`. An on-device durable event queue is a variation on code that already ships on these boards, not new infrastructure.

### 4.2 (Session 7) Mesh channel encryption is on by default, with a publicly known key

`Channels::initDefaultChannel()` (`src/mesh/Channels.cpp:128–134`) sets `channelSettings.psk.bytes[0] = 1` with `defaultpskIndex = 1`, and the key-expansion comment at `:238` states plainly that *"index of 1 means no change vs defaultPSK"*, higher indices merely increment the last byte of the same base key (`:234–238`).

So on a factory-default TrekLink unit the primary channel **is** AES-encrypted over RF, using **Meshtastic's published default PSK**. That is encryption in form without confidentiality in substance: any stock Meshtastic client in radio range decrypts the traffic, including SOS positions.

> **Two different switches, routinely conflated.** The LoRa **channel PSK** protects the RF hop between devices. `moduleConfig.mqtt.encryption_enabled` (§4) decides only whether the packet handed to the *broker* stays encrypted. They are independent, and the correct settings differ, see **D-021**.

---

## 5. Hardware variants

| Variant | Board | `platformio.ini` | MQTT |
|---|---|---|---|
| `treklink-v1` | `treklink-esp32` (ESP32) | `variants/esp32/treklink_v1_0/` | ❌ **compiled out**, `-D MESHTASTIC_EXCLUDE_MQTT=1` (`:10`) |
| `treklink-v2` | `esp32-s3-devkitc-1` | `variants/esp32s3/treklink_v2_0/` | ✅ compiled in |
| `treklink-v3-tbeam` | extends `env:tbeam` | `variants/esp32/treklink_v3_tbeam/` | ✅ compiled in |
| `treklink-v4-supreme` | extends `env:tbeam-s3-core` | `variants/esp32s3/treklink_v4_supreme/` | ✅ compiled in |

All four gate TrekLink code behind `-D TREKLINK_VARIANT`. All carry Wi-Fi silicon. v1 also sets `-D MESHTASTIC_EXCLUDE_POWER_TELEMETRY=1`.

**Per D-005, Stage A targets v2/v3/v4. v1 is out of the demo set.** v1's exclusion is a build-time flag, not a runtime setting, no configuration can enable MQTT on a v1 image.

---

## 6. Portnums

The enum (`src/mesh/generated/meshtastic/portnums.pb.h`) is **stock Meshtastic, unmodified**, zero TrekLink entries. `PRIVATE_APP = 256` is the reserved range for application-specific ports and is currently unused by TrekLink; it is the natural home for a custom SOS PortNum should D-008's firmware option be taken.

`protobufs/` and `meshtestic/` are git submodules (`.gitmodules`) and are **not checked out** in the current working copy. Generated headers under `src/mesh/generated/meshtastic/` are committed and are the readable source of truth for wire format.

---

## 7. Maintenance

Update this file whenever firmware behavior relevant to the platform changes, especially under D-008, where the firmware is no longer static. Every claim must cite `file:line`. If a fact cannot be cited, it does not belong here.

**Downstream consumers**: `treklink-web/specs/gateway-sync/{requirements,design,tasks}.md`, `treklink-firmware/specs/onboard-queue/{requirements,design,tasks}.md`, decisions **D-006**, **D-007**, **D-008**, **D-018**, **D-019**, **D-021**.

**Session 7 additions**: the node-side `mqttQueue`, 16 entries, RAM-only, FIFO, **drop-oldest**, one-per-200 ms drain (§4.1); the `MessageStore` flash-queue precedent that an on-device durable queue should follow (§4.1); default-channel PSK is the *published* Meshtastic default, so RF encryption is present but not confidential (§4.2). Found by direct inspection of `src/mqtt/MQTT.{h,cpp}`, `src/mesh/PointerQueue.h`, `src/MessageStore.{h,cpp}` and `src/mesh/Channels.cpp` while scoping the on-device Stage B queue.

**Session 4 additions**: SOS-beacon priority downgrade after the first packet (§2), `nodeNum` MAC-derivation/stability answering Q8 (§3), `TELEMETRY_APP`'s `oneof` variant ambiguity (§4), and the two-tier cancel-gesture UX distinction (§2), found via a cross-repo audit reading the generated protobuf headers, `NodeDB.cpp`, `PositionModule.cpp`, and the TrekLink-specific modules directly. Logged immediately per the session-based-development convention rather than left in conversation.
