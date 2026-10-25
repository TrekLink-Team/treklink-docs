#!/usr/bin/env python3
"""Commit checksum: a sealed declaration of who committed, with which model, at which stage.

Convention: _docs/01-conventions/07-github-workflow-git-conventions.md §3.6 (D-054).

Every commit a member makes carries one trailer:

    Checksum: <66 hex>      (tk2; 64 hex for the older tk1)

A commit with no trailer is a manual commit: the check passes and the pull
request gets the provenance-review label for a review by hand.

The token is AES-256-GCM under the member's own key, bound to the member code
and the commit subject line as associated data. Format tk2 (66 hex) holds five
bytes: model family, major and minor version, variant (sol, luna, flash, argon
and so on) and stage. The older tk1 (64 hex) holds four bytes, without the
variant; it still verifies, but a model whose approval depends on the variant
is then labelled for a manual audit (D-070).

A model passes only if it is listed in ALLOWLIST below, or belongs to a family
in APPROVED_FAMILIES. There is no version comparison: a model released later
fails until it is added to the list.

What it proves: the token was produced with that member's key for a commit with
that subject, and the declared model and stage were not edited afterwards. What
it does not prove: which model actually wrote the code. The declaration is
still the member's word, now sealed instead of free text.

Commands:
    keygen  --members KhoaDD=ruskicoder,LongLP=lamphilong2004 [--out FILE]
    install [REPO ...]              add the commit-msg hook to each repository
    hook    MSGFILE                 called by the hook; seals the message
    verify  [GIT-LOG-ARGS]          check commits; default the last 20 on HEAD
    audit   [GIT-LOG-ARGS]          verify, and print the decoded model and stage
    ci                              GitHub Actions: check a pull request's commits
    selftest                        check the allowlist and the token rules offline

Configuration, per repository or global:
    git config treklink.member KhoaDD        your member code
    git config treklink.model  claude-opus-5-5   or human; TK_MODEL overrides
    git config treklink.stage  CO            optional; TK_STAGE overrides

Keys are read from TK_CHECKSUM_KEYS (JSON text, used by CI), then
TK_CHECKSUM_KEYS_FILE, then ../.provenance/keys.json relative to the repository
(the capstone folder). Sealing with another member's key, or writing a token by
any other means, is forbidden (D-054).
"""

from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

VERSION_TAG = b"tk1"   # legacy, verify only
VERSION_TAG2 = b"tk2"  # written by the hook since D-070

# Model families. Ids 17 and 18 exist only in tk1 tokens, where every Gemini was
# sealed as "gemini-flash" or "gemini-pro"; tk2 seals Gemini as family 19 with
# its variant.
FAMILIES = {
    "human": 0, "claude-opus": 1, "claude-sonnet": 2, "claude-fable": 3,
    "gpt": 4, "claude-haiku": 16, "gemini-flash": 17, "gemini-pro": 18, "gemini": 19,
}
FAMILY_NAMES = {v: k for k, v in FAMILIES.items()}
LEGACY_FAMILY = {"gemini-flash": "gemini", "gemini-pro": "gemini"}

VARIANTS = {"": 0, "sol": 1, "luna": 2, "terra": 3, "astra": 4, "cyber": 5,
            "flash": 6, "pro": 7, "argon": 8}
VARIANT_NAMES = {v: k for k, v in VARIANTS.items()}

# The model list of chapter 11 §2 (D-070), one entry per model. "approved" may
# write any commit; "ingest" is for reading a codebase only and fails on every
# commit. Anything not listed fails. Edit this table, chapter 11 §2.1 and the
# register together.
APPROVED, INGEST = "approved", "ingest"
ALLOWLIST: dict[tuple[str, int, int, str], str] = {
    **{("claude-sonnet", ma, mi, ""): APPROVED for ma, mi in [(4, 6), (4, 8), (5, 0), (5, 5)]},
    **{("claude-opus", ma, mi, ""): APPROVED for ma, mi in [(4, 6), (4, 7), (4, 8), (5, 0), (5, 5)]},
    **{("claude-haiku", ma, mi, ""): APPROVED for ma, mi in [(5, 0), (5, 5)]},
    ("gpt", 5, 6, "sol"): APPROVED,
    ("gpt", 5, 6, "cyber"): APPROVED,
    ("gpt", 5, 6, "luna"): INGEST,
    ("gpt", 5, 6, "terra"): INGEST,
    ("gpt", 6, 0, ""): APPROVED,
    ("gpt", 6, 0, "sol"): APPROVED,
    ("gpt", 6, 0, "luna"): APPROVED,
    ("gpt", 6, 0, "astra"): APPROVED,
    ("gpt", 6, 1, "sol"): APPROVED,
    ("gemini", 3, 8, "flash"): INGEST,
    ("gemini", 4, 0, "argon"): APPROVED,
}
# Families approved at every version, without a variant: the leader's one
# deliberate wildcard (D-070, rule 3).
APPROVED_FAMILIES = {"claude-fable"}

STAGES = {"SD": 1, "CO": 2, "UT": 3, "RV": 4, "DOC": 5, "CHORE": 6}
STAGE_NAMES = {v: k for k, v in STAGES.items()}
DEFAULT_STAGE = {
    "feat": "CO", "fix": "CO", "refactor": "CO", "perf": "CO", "hotfix": "CO",
    "test": "UT", "docs": "DOC",
    "chore": "CHORE", "ci": "CHORE", "build": "CHORE", "style": "CHORE", "revert": "CHORE",
}

TRAILER_RE = re.compile(r"^Checksum:\s*(\S+)\s*$", re.MULTILINE | re.IGNORECASE)
TYPE_RE = re.compile(r"^(\w+)(\([^)]*\))?!?:")
AI_ATTRIBUTION_RE = re.compile(
    r"^Co-Authored-By:.*(claude|anthropic|openai|chatgpt|gpt-|gemini|copilot|cursor|codex)"
    r"|Generated with \[?(Claude|ChatGPT|Gemini|Copilot|Cursor|Codex)"
    r"|^Claude-Session:",
    re.MULTILINE | re.IGNORECASE,
)
AI_IDENTITY_RE = re.compile(r"noreply@anthropic\.com|^claude$|copilot|chatgpt", re.IGNORECASE)


class ChecksumError(Exception):
    pass


# ── model and subject parsing ────────────────────────────────────────────────

def parse_model(name: str) -> tuple[int, int, int, int]:
    """'claude-opus-5-5' -> (1, 5, 5, 0); 'gpt-6-astra' -> (4, 6, 0, 4); 'human' -> (0, 0, 0, 0).

    The whole name must match: a suffix such as '-preview' or an unknown variant is an error,
    so nothing is silently dropped from the declaration.
    """
    n = name.strip().lower().replace(".", "-").replace("_", "-").replace(" ", "-")
    if n in ("human", "none", "hand-written"):
        return FAMILIES["human"], 0, 0, 0
    m = re.fullmatch(r"(claude-(?:opus|sonnet|fable|haiku)|gpt|gemini)-(\d+)(?:-(\d+))?(?:-([a-z]+))?", n)
    if not m:
        raise ChecksumError(f"unknown model '{name}'; see chapter 11 §2 for the allowed names")
    family, major, minor, variant = m.group(1), int(m.group(2)), int(m.group(3) or 0), m.group(4) or ""
    if variant not in VARIANTS:
        raise ChecksumError(f"unknown variant '{variant}' in '{name}'; one of {', '.join(v for v in VARIANTS if v)}")
    if minor > 255 or major > 255:
        raise ChecksumError(f"model version out of range in '{name}'")
    return FAMILIES[family], major, minor, VARIANTS[variant]


def model_label(family: int, major: int, minor: int, variant: int | None = 0) -> str:
    name = FAMILY_NAMES.get(family, f"unknown-{family}")
    if name == "human":
        return name
    suffix = "-?" if variant is None else (f"-{VARIANT_NAMES.get(variant, '?')}" if variant else "")
    return f"{name}-{major}.{minor}{suffix}"


def model_status(family: int, major: int, minor: int, variant: int | None) -> str:
    """Returns 'human', 'approved', 'ingest', 'off-list', or 'legacy' for a tk1 token whose
    approval depends on the variant it cannot carry. `variant` is None for a tk1 token."""
    name = FAMILY_NAMES.get(family)
    if name == "human":
        return "human"
    if name is None:
        return "off-list"
    name = LEGACY_FAMILY.get(name, name)
    if variant is not None:
        if name in APPROVED_FAMILIES and variant == 0:
            return "approved"
        return ALLOWLIST.get((name, major, minor, VARIANT_NAMES.get(variant, "?")), "off-list")
    if name in APPROVED_FAMILIES:
        return "approved"
    candidates = {v: s for (f, ma, mi, v), s in ALLOWLIST.items() if (f, ma, mi) == (name, major, minor)}
    if candidates.get("") == APPROVED:
        return "approved"
    if APPROVED in candidates.values():
        return "legacy"
    if INGEST in candidates.values():
        return "ingest"
    return "off-list"


def subject_of(message: str) -> str:
    for line in message.splitlines():
        if line.startswith("#"):
            continue
        if line.strip():
            return line.strip()
    return ""


def commit_type(subject: str) -> str:
    m = TYPE_RE.match(subject)
    return m.group(1).lower() if m else ""


def find_token(message: str) -> str | None:
    found = TRAILER_RE.findall(message)
    return found[-1] if found else None


# ── keys and crypto ──────────────────────────────────────────────────────────

def _aesgcm(key_hex: str):
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise ChecksumError("python package 'cryptography' is missing: pip install cryptography") from exc
    key = bytes.fromhex(key_hex)
    if len(key) != 32:
        raise ChecksumError("a member key must be 32 bytes (64 hex)")
    return AESGCM(key)


def _aad(member: str, subject: str, tag: bytes = VERSION_TAG2) -> bytes:
    return tag + b"|" + member.encode() + b"|" + subject.encode()


def seal(key_hex: str, member: str, subject: str, model: str, stage: str) -> str:
    """Always writes tk2: 12-byte nonce, 5-byte ciphertext, 16-byte tag, 66 hex."""
    family, major, minor, variant = parse_model(model)
    if stage not in STAGES:
        raise ChecksumError(f"unknown stage '{stage}'; one of {', '.join(STAGES)}")
    nonce = secrets.token_bytes(12)
    plain = bytes([family, major, minor, variant, STAGES[stage]])
    ct = _aesgcm(key_hex).encrypt(nonce, plain, _aad(member, subject))
    return (nonce + ct).hex()


def open_token(keys: dict, token: str, subject: str) -> tuple[str, tuple] | None:
    """Returns (member, (family, major, minor, variant, stage)) or None if no key opens it.
    `variant` is None for a tk1 token (64 hex), which never carried it."""
    if re.fullmatch(r"[0-9a-fA-F]{66}", token):
        tag = VERSION_TAG2
    elif re.fullmatch(r"[0-9a-fA-F]{64}", token):
        tag = VERSION_TAG
    else:
        return None
    raw = bytes.fromhex(token)
    for member, entry in keys["members"].items():
        try:
            pt = _aesgcm(entry["key"]).decrypt(raw[:12], raw[12:], _aad(member, subject, tag))
        except Exception:
            continue
        if tag == VERSION_TAG:
            family, major, minor, stage = pt
            return member, (family, major, minor, None, stage)
        return member, tuple(pt)
    return None


def load_keys(repo: Path | None = None) -> dict:
    text = os.environ.get("TK_CHECKSUM_KEYS")
    if not text:
        candidates = []
        if os.environ.get("TK_CHECKSUM_KEYS_FILE"):
            candidates.append(Path(os.environ["TK_CHECKSUM_KEYS_FILE"]))
        if repo:
            candidates.append(repo.parent / ".provenance" / "keys.json")
        for c in candidates:
            if c.is_file():
                text = c.read_text()
                break
    if not text:
        raise ChecksumError("no keys: set TK_CHECKSUM_KEYS_FILE or keep capstone/.provenance/keys.json")
    keys = json.loads(text)
    if "members" not in keys:
        raise ChecksumError("keys file has no 'members' object")
    return keys


# ── git helpers ──────────────────────────────────────────────────────────────

def git(*args: str, cwd: Path | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout


def git_config(name: str) -> str:
    r = subprocess.run(["git", "config", "--get", name], capture_output=True, text=True)
    return r.stdout.strip()


def repo_root() -> Path:
    return Path(git("rev-parse", "--show-toplevel").strip())


# ── commands ─────────────────────────────────────────────────────────────────

def cmd_keygen(args: list[str]) -> int:
    members, out = None, None
    it = iter(args)
    for a in it:
        if a == "--members":
            members = next(it)
        elif a == "--out":
            out = Path(next(it))
    if not members:
        raise ChecksumError("keygen needs --members CODE=github,CODE=github")
    data = {"version": 1, "members": {}}
    for pair in members.split(","):
        code, login = pair.split("=")
        data["members"][code.strip()] = {"github": login.strip(), "key": secrets.token_hex(32)}
    text = json.dumps(data, indent=2) + "\n"
    if out:
        if out.exists():
            raise ChecksumError(f"{out} exists; rotating keys invalidates every sealed commit, remove it by hand first")
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text)
        print(f"wrote {out}")
    else:
        sys.stdout.write(text)
    return 0


HOOK = """#!/bin/sh
# TrekLink commit checksum (D-054). Installed by tk_checksum.py install.
exec python3 "{script}" hook "$1"
"""


def cmd_install(args: list[str]) -> int:
    script = Path(__file__).resolve()
    repos = [Path(a).resolve() for a in args] or [repo_root()]
    for repo in repos:
        hooks = Path(git("rev-parse", "--git-path", "hooks", cwd=repo).strip())
        if not hooks.is_absolute():
            hooks = repo / hooks
        hooks.mkdir(parents=True, exist_ok=True)
        hook = hooks / "commit-msg"
        if hook.exists() and "tk_checksum" not in hook.read_text():
            print(f"{repo}: a different commit-msg hook exists, not replaced")
            continue
        hook.write_text(HOOK.format(script=script))
        hook.chmod(0o755)
        print(f"{repo}: commit-msg hook installed")
    return 0


def cmd_hook(args: list[str]) -> int:
    msg_file = Path(args[0])
    message = msg_file.read_text()
    subject = subject_of(message)
    if not subject or subject.startswith(("Merge ", "fixup! ", "squash! ")):
        return 0
    member = git_config("treklink.member")
    model = os.environ.get("TK_MODEL") or git_config("treklink.model")
    if not member or not model:
        print("tk_checksum: treklink.member or treklink.model not set; commit left unsealed "
              "(reviewed by hand)", file=sys.stderr)
        return 0
    stage = (os.environ.get("TK_STAGE") or git_config("treklink.stage")
             or DEFAULT_STAGE.get(commit_type(subject), "CO")).upper()
    keys = load_keys(repo_root())
    entry = keys["members"].get(member)
    if not entry:
        raise ChecksumError(f"member '{member}' has no key in keys.json")
    token = seal(entry["key"], member, subject, model, stage)
    status = model_status(*parse_model(model))
    if status not in ("approved", "human"):
        print(f"tk_checksum: '{model}' is not allowed on a commit (chapter 11 §2, D-070); "
              "it is sealed as declared and the pull request check will fail", file=sys.stderr)
    subprocess.run(["git", "interpret-trailers", "--in-place", "--if-exists", "replace",
                    "--trailer", f"Checksum: {token}", str(msg_file)], check=True)
    return 0


_RANK = {"ok": 0, "label": 1, "fail": 2}


def _check_token(keys: dict, message: str, login: str | None) -> tuple[str, str, tuple | None]:
    subject = subject_of(message)
    token = find_token(message)
    if token is None:
        # No trailer, or an empty one: a manual commit. Labelled for a review by hand, never failed.
        return "label", "unsealed, review by hand", None
    opened = open_token(keys, token, subject)
    if opened is None:
        return "fail", "token does not verify under any member key", None
    member, decoded = opened
    expected = keys["members"][member].get("github", "")
    if login and expected and login.lower() != expected.lower():
        return "fail", f"token sealed by {member}, commit pushed by {login}", decoded
    family, major, minor, variant, stage = decoded
    if stage not in STAGE_NAMES:
        return "fail", "unknown stage in token", decoded
    status = model_status(family, major, minor, variant)
    if status == "off-list":
        return "fail", "model not on the allowlist (chapter 11 §2, D-070)", decoded
    if status == "ingest":
        return "fail", "ingest-only model declared on a commit (chapter 11 §2.2, D-070)", decoded
    if status == "legacy":
        return "label", f"sealed by {member} in the old tk1 format, variant unknown, audit by hand", decoded
    if not login:
        return "label", f"sealed by {member}, author not linked to a GitHub account", decoded
    return "ok", f"sealed by {member}", decoded


def check_commit(keys: dict, message: str, login: str | None, author: str) -> tuple[str, str, tuple | None]:
    """Returns (level, reason, decoded). level is ok, label or fail; the worse finding wins."""
    level, reason, decoded = _check_token(keys, message, login)
    if AI_ATTRIBUTION_RE.search(message) or AI_IDENTITY_RE.search(author):
        attribution = "AI attribution in the commit (D-049)"
        if _RANK[level] < _RANK["label"]:
            return "label", attribution, decoded
        reason = f"{reason}; {attribution}"
    return level, reason, decoded


def _local_commits(rev_args: list[str]) -> list[tuple[str, str, str]]:
    sep = "\x1e"
    out = git("log", "--no-merges", f"--format=%H%x1f%an <%ae>%x1f%B{sep}", *rev_args)
    rows = []
    for chunk in out.split(sep):
        chunk = chunk.strip("\n")
        if not chunk:
            continue
        sha, author, body = chunk.split("\x1f", 2)
        rows.append((sha, author, body))
    return rows


def cmd_verify(args: list[str], show: bool) -> int:
    rev_args = args or ["-20", "HEAD"]
    keys = load_keys(repo_root())
    logins = {m: e.get("github") for m, e in keys["members"].items()}
    failed = 0
    for sha, author, body in _local_commits(rev_args):
        opened = None
        token = find_token(body)
        if token:
            opened = open_token(keys, token, subject_of(body))
        login = logins.get(opened[0]) if opened else None
        level, reason, decoded = check_commit(keys, body, login, author)
        extra = ""
        if show and decoded:
            extra = f"  {model_label(*decoded[:4])} {STAGE_NAMES.get(decoded[4], '?')}"
        print(f"{level:5} {sha[:10]} {reason}{extra}  | {subject_of(body)[:60]}")
        failed += level == "fail"
    return 1 if failed else 0


def _api(method: str, url: str, token: str, body: dict | None = None):
    req = urllib.request.Request(url, method=method, data=json.dumps(body).encode() if body else None)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Accept", "application/vnd.github+json")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read() or b"null")


def cmd_ci(_: list[str]) -> int:
    gh_token = os.environ["GITHUB_TOKEN"]
    repo = os.environ["GITHUB_REPOSITORY"]
    pr = os.environ["PR_NUMBER"]
    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    keys = load_keys()
    commits, page = [], 1
    while True:
        batch = _api("GET", f"{api}/repos/{repo}/pulls/{pr}/commits?per_page=100&page={page}", gh_token)
        commits += batch
        if len(batch) < 100:
            break
        page += 1

    rows, fails, labels = [], 0, 0
    for c in commits:
        if len(c.get("parents", [])) > 1:
            continue
        user = c.get("author") or {}
        if user.get("type") == "Bot" or (user.get("login") or "").endswith("[bot]"):
            continue
        meta = c["commit"]["author"]
        level, reason, _ = check_commit(keys, c["commit"]["message"], user.get("login"),
                                        f"{meta['name']} <{meta['email']}>")
        rows.append((c["sha"][:10], level, reason, subject_of(c["commit"]["message"])[:70]))
        fails += level == "fail"
        # AI attribution is labelled even when the commit also fails for another reason.
        labels += level == "label" or "attribution" in reason
        if level == "fail":
            print(f"::error title=Commit checksum::{c['sha'][:10]} {reason}")
        elif level == "label":
            print(f"::warning title=Commit checksum::{c['sha'][:10]} {reason}")

    # The decoded model and stage are deliberately not printed: the repositories
    # are public and the trailer keeps the model inside the token (D-054).
    summary = ["## Commit checksum", "", "| Commit | Result | Reason | Subject |", "|---|---|---|---|"]
    summary += [f"| `{s}` | {lv} | {r} | {subj.replace('|', '/')} |" for s, lv, r, subj in rows]
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as fh:
            fh.write("\n".join(summary) + "\n")
    print("\n".join(summary))

    if labels:
        try:
            _api("POST", f"{api}/repos/{repo}/labels", gh_token,
                 {"name": "provenance-review", "color": "d4c5f9",
                  "description": "Unsealed or AI-attributed commit, review by hand (D-054)"})
        except urllib.error.HTTPError as exc:
            if exc.code != 422:
                raise
        _api("POST", f"{api}/repos/{repo}/issues/{pr}/labels", gh_token, {"labels": ["provenance-review"]})
    return 1 if fails else 0


SELFTEST_STATUS = [
    # Every allowlisted model, and the near misses a version comparison would let through.
    ("claude-opus-4-6", "approved"), ("claude-opus-4-7", "approved"), ("claude-opus-4-8", "approved"),
    ("claude-opus-5", "approved"), ("claude-opus-5-5", "approved"), ("claude-opus-4-5", "off-list"),
    ("claude-opus-5-6", "off-list"), ("claude-opus-6", "off-list"), ("claude-opus-9-9", "off-list"),
    ("claude-sonnet-4-6", "approved"), ("claude-sonnet-4-8", "approved"), ("claude-sonnet-5", "approved"),
    ("claude-sonnet-5-5", "approved"), ("claude-sonnet-4-7", "off-list"), ("claude-sonnet-6", "off-list"),
    ("claude-haiku-5", "approved"), ("claude-haiku-5-5", "approved"), ("claude-haiku-4-5", "off-list"),
    ("claude-fable-5", "approved"), ("claude-fable-5-1", "approved"), ("claude-fable-7", "approved"),
    ("claude-fable-5-1-sol", "off-list"),
    ("gpt-5-6-sol", "approved"), ("gpt-5-6-cyber", "approved"), ("gpt-5-6-luna", "ingest"),
    ("gpt-5-6-terra", "ingest"), ("gpt-5-6", "off-list"), ("gpt-5-6-astra", "off-list"),
    ("gpt-6", "approved"), ("gpt-6-sol", "approved"), ("gpt-6-luna", "approved"), ("gpt-6-astra", "approved"),
    ("gpt-6-terra", "off-list"), ("gpt-6-1-sol", "approved"), ("gpt-6-1", "off-list"), ("gpt-5-7", "off-list"),
    ("gpt-9-9-sol", "off-list"),
    ("gemini-3.8-flash", "ingest"), ("gemini-4-argon", "approved"), ("gemini-3-1-pro", "off-list"),
    ("gemini-4-flash", "off-list"), ("human", "human"),
]
SELFTEST_UNPARSABLE = ["claude-opus-5-5-preview", "gpt-6-nova", "llama-4", "claude-opus"]


def cmd_selftest(_: list[str]) -> int:
    failures = []
    for name, want in SELFTEST_STATUS:
        got = model_status(*parse_model(name))
        if got != want:
            failures.append(f"{name}: expected {want}, got {got}")
    for name in SELFTEST_UNPARSABLE:
        try:
            parse_model(name)
            failures.append(f"{name}: parsed, expected an error")
        except ChecksumError:
            pass
    keys = {"members": {"A": {"github": "a", "key": secrets.token_hex(32)},
                        "B": {"github": "b", "key": secrets.token_hex(32)}}}
    subject = "feat(TK-1): add x"

    def msg(token: str, subj: str = subject) -> str:
        return f"{subj}\n\nChecksum: {token}\n"

    def legacy(model: tuple[int, int, int], stage: str = "CO") -> str:
        nonce = secrets.token_bytes(12)
        ct = _aesgcm(keys["members"]["A"]["key"]).encrypt(
            nonce, bytes([*model, STAGES[stage]]), _aad("A", subject, VERSION_TAG))
        return (nonce + ct).hex()

    good = seal(keys["members"]["A"]["key"], "A", subject, "claude-opus-5-5", "CO")
    cases = [
        ("tk2 approved", msg(good), "a", "ok"),
        ("pushed by another member", msg(good), "b", "fail"),
        ("subject edited", msg(good, "feat(TK-1): add y"), "a", "fail"),
        ("token edited", msg(good[:-1] + ("0" if good[-1] != "0" else "1")), "a", "fail"),
        ("unsealed (manual commit)", subject, "a", "label"),
        ("empty trailer", f"{subject}\n\nChecksum: \n", "a", "label"),
        ("ingest-only on docs", msg(seal(keys["members"]["A"]["key"], "A", subject, "gemini-3-8-flash", "DOC")), "a", "fail"),
        ("off-list", msg(seal(keys["members"]["A"]["key"], "A", subject, "claude-opus-6", "CO")), "a", "fail"),
        ("tk1 opus 5.5", msg(legacy((1, 5, 5))), "a", "ok"),
        ("tk1 gpt 6.0", msg(legacy((4, 6, 0))), "a", "ok"),
        ("tk1 gpt 5.6, variant unknown", msg(legacy((4, 5, 6))), "a", "label"),
        ("tk1 gemini-flash 3.8", msg(legacy((17, 3, 8))), "a", "fail"),
        ("tk1 opus 9.9", msg(legacy((1, 9, 9))), "a", "fail"),
        ("approved with AI attribution", msg(good) + "Co-Authored-By: Claude <noreply@anthropic.com>\n", "a", "label"),
        ("unsealed with AI attribution", subject + "\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n", "a", "label"),
    ]
    for label, message, login, want in cases:
        got = check_commit(keys, message, login, "x <x@example.com>")[0]
        if got != want:
            failures.append(f"{label}: expected {want}, got {got}")
    for line in failures:
        print(f"FAIL {line}")
    total = len(SELFTEST_STATUS) + len(SELFTEST_UNPARSABLE) + len(cases)
    print(f"selftest: {total - len(failures)} of {total} passed")
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    cmd, args = argv[0], argv[1:]
    try:
        if cmd == "keygen":
            return cmd_keygen(args)
        if cmd == "install":
            return cmd_install(args)
        if cmd == "hook":
            return cmd_hook(args)
        if cmd == "verify":
            return cmd_verify(args, show=False)
        if cmd == "audit":
            return cmd_verify(args, show=True)
        if cmd == "ci":
            return cmd_ci(args)
        if cmd == "selftest":
            return cmd_selftest(args)
    except ChecksumError as exc:
        print(f"tk_checksum: {exc}", file=sys.stderr)
        return 1
    print(f"unknown command '{cmd}'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
