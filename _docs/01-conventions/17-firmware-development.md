# 17: Firmware Development

How a change to `treklink-firmware` is made, checked on hardware and merged. Recorded as **D-077**.

This chapter holds the process: change classes, the fix loop, the hardware-run gate, evidence
rules for agents, review, the upstream policy and bench safety. Everything else has one home
elsewhere:

| Topic | Home |
|---|---|
| Embedded C/C++ practice for this firmware | `treklink-firmware/docs/coding-conventions.md` |
| Build, flash and test commands | `treklink-firmware/docs/build-and-flash.md` |
| What each variant is (board, env, pins, IMU, alarms) | `treklink-firmware/docs/variants.md` |
| What the firmware puts on the wire | [`../00-project-context/04-firmware-ground-truth.md`](../00-project-context/04-firmware-ground-truth.md) |
| Firmware repository layout | [`09-doc-driven-scaffold-and-ssot-conventions.md`](09-doc-driven-scaffold-and-ssot-conventions.md) §1.1 |
| Git, commits, Jira, wording, agent discipline | Chapters 07, 10, 14 and 08, unchanged for firmware |

**Why this chapter exists.** The 2026-10-29 v2 hardware run
(`treklink-firmware/docs/test-runs/2026-10-29-v2-hardware-run.md`) found that any stock beep
silences the SOS buzzer (F2), that SOS vibration stops after three pulses (F3), and that fall
detection cannot reach its pre-alarm (F4, F5). The variant specs were marked `implemented` with
every task ticked (`treklink-firmware/specs/README.md`). Nothing on the path to merge had run the
behaviour on a device.

---

## 1. Change classes

| Class | What it covers | Gate |
|---|---|---|
| **S**, safety path | Anything that can change whether an SOS or fall alarm is raised, heard, felt, seen, sent or cancelled, or whether the device stays powered. TrekLink files, in the D-086 layout once its branch lands: everything under `treklink/src/` except `treklink/src/test/`, and every file in `variants/<arch>/treklink_*/` (on the 2.7.19 snapshot: `src/modules/TrekLink*`, `src/modules/FallDetectionModule*`, `src/modules/FallSensorInterface.h`, `src/modules/BuzzerManager.h`, `src/modules/sensors/`, `src/input/TrekLink*`, `src/mqtt/TrekLink*` and the TrekLink variant files). Stock code that shares a resource with them: LEDC and `tone()`, the buzzer, vibrator and LED pins, the IMU and its I2C or SPI bus, screen banners and input routing, power, sleep and shutdown. | §2 in full, including the hardware run of §3 |
| **N**, normal | Everything else: UI text, log wording, documentation, changes confined to `test/` or `treklink/tools/`, non-TrekLink variants. | §2 steps 1 to 6 and 8; a hardware run is optional |

The class follows from the files and resources a change touches, not from its intent. When in
doubt, the change is class S. The PR states its class.

---

## 2. The fix loop

1. **Finding.** A defect has an ID: a finding in a test run (`F4` of
   `2026-10-29-v2-hardware-run`) or a register row. No fix without a recorded finding. A defect found
   while fixing another one gets its own finding first.
2. **Root cause.** Stated with `file:line` at the base commit and tagged KNOWN, INFERRED or UNKNOWN
   (§4). Where hardware reproduces the defect, cite the log line.
3. **Spec.** Update the requirement or design the fix changes (`specs/variants/vN/`,
   `specs/sos/`, `specs/fall-detection/`) on the same branch, spec commit first (chapter 07 §2.3).
   If the fix creates behaviour no spec describes, write the requirement before the code.
4. **Branch.** One defect per `fix/<slug>` branch from `dev`. Two defects in the same lines may
   share a branch when the PR lists both finding IDs.
5. **Testable core.** Logic that can run without hardware (thresholds, state machines, timing
   windows, queue policy) moves into a platform-free core with a `native` test, following
   `treklink/src/queue/TrekLinkQueueCore.cpp` and `test/treklink_queue/`. The test reproduces the defect
   and fails before the fix. Rules: `coding-conventions.md`.
6. **Build matrix.** `pio run -e <env> -t buildprog` for every env the change can reach, plus the
   stock regression env for v3 and v4 (`build-and-flash.md`). A change to a shared TrekLink file
   reaches `treklink-v2`, `treklink-v3` and `treklink-v4`, plus the overlay check
   (`treklink/tools/check_overlay.py`). `pio test -e native -f treklink_queue` when a core changes.
7. **Hardware run**, class S: §3.
8. **Pull request.** The body lists the class, the finding IDs, the root cause, the build matrix
   result, the native test output and, for class S, the test-run file.
9. **After merge**, in the same pass: the test-run index row, `hw_verified` in the spec
   frontmatter, the register row's status, and ground truth if a wire fact changed.

---

## 3. The hardware-run gate

A class S pull request does not merge without a test-run file on the same branch,
`docs/test-runs/YYYY-MM-DD-<variant>-<topic>.md`, that shows for **each affected variant**:

1. **The image.** The version string from the boot log, `<version>.<sha>`, whose SHA is the
   branch head that was flashed, and any extra build flags. A run on a diagnostic image
   (for example `-DARDUINO_USB_CDC_ON_BOOT=1`) counts only for behaviour the flag cannot affect;
   say so per behaviour.
2. **The unit and conditions.** Node ID, boot type (cold power-up or warm reset; F7 shows they
   differ), GPS fix, battery, what else was on the bench.
3. **The finding, re-run.** The reproduction steps of each finding the PR fixes, now passing, with
   the log line.
4. **The regression set**, each row marked pass, fail or not run:

   | Check | Applies to |
   |---|---|
   | Cold power-up and warm reset: IMU detected and the expected driver path logged | v2, v4 |
   | SOS trigger: buzzer, vibration, LED, banner, packets sent | all |
   | SOS trigger after a stock button beep | v1, v2 (F2) |
   | SOS cancel: outputs off, cancel state shown | all |
   | Fall drop with the screen on, and with the screen timed out | variants that run fall detection, once F4 is fixed |
   | Long press of each button: no unintended shutdown | all |
   | Power latch holds after the flash and after a reboot | v2 |

5. **Raw logs** committed under `docs/test-runs/logs/<date>-<variant>/`, ASCII only, checked for
   secrets before the commit.

The member holding the unit runs the test; an agent may flash it and read the log (§7). A variant
with no unit available is reported as not run: the PR says so, the register row stays open, and
`hw_verified` is not raised for that variant. The leader decides whether such a PR merges.

A run file is closed once written. A failed run stays as it is, and the rerun is a new file.

---

## 4. Evidence rules for agents

These extend the epistemic anchor of chapter 08 for firmware, where a wrong assumption costs a
field failure rather than a failed test.

1. **Tag every behaviour claim.** KNOWN: code `file:line` at a named commit, or a line in a
   committed log. INFERRED: with a confidence. UNKNOWN: flagged before acting on it.
2. **"Fixed", "works" and "verified" need a hardware log line.** A build proves the code compiles; a
   native test proves the logic. Neither proves the device behaves.
3. **Cite the library version in use.** Framework and library claims cite the file inside the
   package PlatformIO actually installs for the env: Arduino-ESP32 2.0.17 under
   `~/.platformio/packages/framework-arduinoespressif32/` for `platformio/espressif32@6.13.0`
   (`variants/esp32/esp32-common.ini:8`), or the version pinned in `platformio.ini`. Web
   documentation for another version is not evidence: Arduino-ESP32 3.x rewrote the LEDC API.
4. **Comments are not evidence.** `BuzzerManager.h:100` (2.7.19 tree, now `treklink/src/alarm/BuzzerManager.h`) says `write()` "only works if
   caller is current owner"; the code at `:102-112` checks only that some owner exists. Read the
   code.
5. **Map shared resources before changing them.** List every other user of the resource in stock
   and TrekLink code: the LEDC channel and `tone()`, the pin, the I2C address and driver singleton,
   the NVS namespace, screen banners and input routing. F2, F5 and F7 each sit in the interaction
   between TrekLink and stock code, not in either alone.
6. **Hardware facts cite two sources.** Pins, buses and chips cite the `variant.h` line and the
   schematic or vendor document. When they disagree, a hardware run decides and ground truth §5
   records it (the v4 QMI8658 bus).
7. **A ticked task is not a working feature.** It means code was written.
8. **Quote logs, do not paraphrase them.** Evidence is the log line with `file:line`.
9. **Ask before touching a unit.** An agent does not flash, reset or open the serial port of a unit
   until the member says it is ready (§7). Chapter 08's circuit breakers apply unchanged.

---

## 5. Reviewing a firmware pull request

The reviewer checks, beyond chapter 07 §5.4:

- The class is stated and matches §1.
- Each finding ID resolves to a test run or register row, and the spec commit precedes the code.
- Every shared resource the change touches is listed with its other users (§4 rule 5).
- The build matrix covers every reachable env, and the native test output is pasted.
- Class S: the test-run file exists, its image SHA matches the branch head, and every regression
  row is marked. A "not run" row is acceptable only with a reason.
- The code follows `treklink-firmware/docs/coding-conventions.md`.

---

## 6. Upstream: `meshtastic/firmware`

**Base.** Once the D-086 branch (`chore/overlay-on-upstream-2-7-26`) lands as `dev`,
`treklink-firmware` sits on real upstream history: the TrekLink commits are a linear series on top of
the stable tag `v2.7.26.54e0d8d`, recorded in `treklink/UPSTREAM`, with the architecture in
`specs/architecture/` and the old snapshot (`91134a2`, tree of upstream `develop` at `538a5f0df`,
2.7.19) kept as tag `archive/pre-overlay`. Until then `dev` is that snapshot, and the paths below name
the overlay layout of the branch. The 2.7.26 platform is `platformio/espressif32@6.13.0`
(upstream `variants/esp32/esp32-common.ini:8` at `v2.7.26.54e0d8d`).
`v2.8.1` (2026-10-01) is still an Alpha after two revoked 2.8.0 builds (checked 2026-10-31).

Rules:

1. **Fixes land in `treklink-firmware` `dev` first**, through §2.
2. **A stock bug still present at the latest stable release** gets an issue on
   `meshtastic/firmware` with the reproduction, once the leader approves the filing. A pull request
   upstream only if the leader decides.
3. **A stock bug upstream already fixed is not fixed in the fork.** It arrives with the sync. Known
   cases: the compass calibration screen that cannot be left (F9; `STOP_ALERT_FRAME` calls
   `setFrames()` from `v2.7.20`) and RAM-only compass calibration (saved to flash by upstream #10166,
   in `v2.7.26`).
4. **Sync by rebase, before fixes that the new base would change.** A stable release is taken on a
   `chore/upstream-sync-<version>` branch: `git rebase --onto <new tag> <old tag>`, the overlay check
   (`treklink/tools/check_overlay.py --against <new tag>` lists every override whose stock code moved),
   the build matrix and the full regression set of §3 on every variant with a unit. Record the new tag
   in `treklink/UPSTREAM` and in this section. (D-086 reversed D-077's order: the 2.7.26 move came
   before the class S fixes.)
5. **The 2.8 line is not a sync target while it is Alpha.** It moves ESP32 builds from
   `platformio/espressif32@6.13.0` (2.7.26) to the pioarduino `55.03.311` platform (Arduino-ESP32 3.x), whose
   pin-based LEDC API needs `BuzzerManager` ported.
6. **No stock file is edited.** TrekLink changes stock behaviour from the overlay only: upstream
   hooks and defines, configuration defaults, objects created or observed at start-up, or a linker
   wrap, each catalogued in `specs/architecture/design.md` §4.2 with the stock line it depends on.
   The overlay check fails on any other change to a stock path (D-086).

---

## 7. Bench safety

Hardware details live in `treklink-firmware/docs/build-and-flash.md`; these rules protect the unit
and the evidence.

1. **v2 power latch.** Any reset releases the latch on `IO9_PWR_EN`, so the member holds or clamps
   the power button before a flash or a reset and keeps it held until the board has booted.
2. **Flash the app, keep the data.** Flashing with esptool at bootloader `0x0`, partitions
   `0x8000`, `boot_app0` `0xe000` and app `0x10000` keeps NVS and LittleFS, so a unit keeps its field
   state (for example the stored fall calibration of F6). An erase is a deliberate step, recorded in
   the run file.
3. **Do not reset by opening the port.** On the ESP32-S3 USB-JTAG port, DTR low with RTS high resets
   the chip. Serial tools keep both lines asserted, and Linux `ModemManager` is stopped before a v2
   is connected.
4. **The v2 stock image has no USB console** (F1). Log capture needs the diagnostic flag, recorded
   in the run file per §3 rule 1.
5. **Say the boot type.** Every log names whether it follows a cold power-up or a warm reset.

The flashing and serial tools that automate these rules are follow-up work; until they land, the
commands in `build-and-flash.md` apply.
