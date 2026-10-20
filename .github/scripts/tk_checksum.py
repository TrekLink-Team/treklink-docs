#!/usr/bin/env python3
"""Commit checksum: a sealed declaration of who committed, with which model, at which stage.

Convention: _docs/01-conventions/07-github-workflow-git-conventions.md §3.6 (D-054).

Every commit a member makes carries one trailer:

    Checksum: <64 hex>

The token is AES-256-GCM under the member's own key. It holds four bytes,
model family, major and minor version, and stage, and is bound to the member
code and the commit subject line as associated data. The 64 hex characters are
the 12-byte nonce, the 4-byte ciphertext and the 16-byte tag.

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

VERSION_TAG = b"tk1"

# Model families. Approved: Claude Opus and Sonnet from 4.8, Claude Fable from
# 5.1, GPT from 5.6. Restricted: never on feat or fix commits. Chapter 11 §2.
FAMILIES = {
    "human": 0, "claude-opus": 1, "claude-sonnet": 2, "claude-fable": 3,
    "gpt": 4, "claude-haiku": 16, "gemini-flash": 17, "gemini-pro": 18,
}
FAMILY_NAMES = {v: k for k, v in FAMILIES.items()}
APPROVED_FLOOR = {"claude-opus": (4, 8), "claude-sonnet": (4, 8), "claude-fable": (5, 1), "gpt": (5, 6)}
RESTRICTED = {"claude-haiku", "gemini-flash", "gemini-pro"}

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

def parse_model(name: str) -> tuple[int, int, int]:
    """'claude-opus-5-5' -> (1, 5, 5); 'gpt-6-astra' -> (4, 6, 0); 'human' -> (0, 0, 0)."""
    n = name.strip().lower().replace(".", "-").replace("_", "-").replace(" ", "-")
    if n in ("human", "none", "hand-written"):
        return FAMILIES["human"], 0, 0
    m = re.match(r"^(claude-(?:opus|sonnet|fable|haiku)|gpt|gemini)-(\d+)(?:-(\d+))?(?:-([a-z]+))?", n)
    if not m:
        raise ChecksumError(f"unknown model '{name}'; see chapter 11 §2 for the allowed names")
    family, major, minor = m.group(1), int(m.group(2)), int(m.group(3) or 0)
    if family == "gemini":
        family = "gemini-pro" if "pro" in n else "gemini-flash"
    if minor > 255 or major > 255:
        raise ChecksumError(f"model version out of range in '{name}'")
    return FAMILIES[family], major, minor


def model_label(family: int, major: int, minor: int) -> str:
    name = FAMILY_NAMES.get(family, f"unknown-{family}")
    return name if name == "human" else f"{name}-{major}.{minor}"


def model_status(family: int, major: int, minor: int) -> str:
    """Returns 'human', 'approved', 'restricted' or 'off-list'."""
    name = FAMILY_NAMES.get(family)
    if name == "human":
        return "human"
    if name in RESTRICTED:
        return "restricted"
    floor = APPROVED_FLOOR.get(name or "")
    if floor and (major, minor) >= floor:
        return "approved"
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


def _aad(member: str, subject: str) -> bytes:
    return VERSION_TAG + b"|" + member.encode() + b"|" + subject.encode()


def seal(key_hex: str, member: str, subject: str, model: str, stage: str) -> str:
    family, major, minor = parse_model(model)
    if stage not in STAGES:
        raise ChecksumError(f"unknown stage '{stage}'; one of {', '.join(STAGES)}")
    nonce = secrets.token_bytes(12)
    ct = _aesgcm(key_hex).encrypt(nonce, bytes([family, major, minor, STAGES[stage]]), _aad(member, subject))
    return (nonce + ct).hex()


def open_token(keys: dict, token: str, subject: str) -> tuple[str, tuple[int, int, int, int]] | None:
    """Returns (member, (family, major, minor, stage)) or None if no key opens it."""
    if not re.fullmatch(r"[0-9a-fA-F]{64}", token):
        return None
    raw = bytes.fromhex(token)
    for member, entry in keys["members"].items():
        try:
            pt = _aesgcm(entry["key"]).decrypt(raw[:12], raw[12:], _aad(member, subject))
        except Exception:
            continue
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
    if status == "off-list" or (status == "restricted" and commit_type(subject) in ("feat", "fix", "hotfix")):
        print(f"tk_checksum: '{model}' is not allowed on this commit (chapter 11 §2); "
              "it is sealed as declared and the pull request check will fail", file=sys.stderr)
    subprocess.run(["git", "interpret-trailers", "--in-place", "--if-exists", "replace",
                    "--trailer", f"Checksum: {token}", str(msg_file)], check=True)
    return 0


def check_commit(keys: dict, message: str, login: str | None, author: str) -> tuple[str, str, tuple | None]:
    """Returns (level, reason, decoded). level is ok, label or fail."""
    subject = subject_of(message)
    if AI_ATTRIBUTION_RE.search(message) or AI_IDENTITY_RE.search(author):
        return "label", "AI attribution in the commit (D-049)", None
    token = find_token(message)
    if token is None:
        return "label", "unsealed, review by hand", None
    opened = open_token(keys, token, subject)
    if opened is None:
        return "fail", "token does not verify under any member key", None
    member, decoded = opened
    expected = keys["members"][member].get("github", "")
    if login and expected and login.lower() != expected.lower():
        return "fail", f"token sealed by {member}, commit pushed by {login}", decoded
    if not login:
        return "label", f"sealed by {member}, author not linked to a GitHub account", decoded
    family, major, minor, stage = decoded
    status = model_status(family, major, minor)
    if stage not in STAGE_NAMES:
        return "fail", "unknown stage in token", decoded
    if status == "off-list":
        return "fail", "model outside the approved list (chapter 11 §2)", decoded
    if status == "restricted" and commit_type(subject) in ("feat", "fix", "hotfix"):
        return "fail", "restricted model on a feat or fix commit (chapter 11 §2.2)", decoded
    return "ok", f"sealed by {member}", decoded


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
            extra = f"  {model_label(*decoded[:3])} {STAGE_NAMES.get(decoded[3], '?')}"
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
        labels += level == "label"
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
    except ChecksumError as exc:
        print(f"tk_checksum: {exc}", file=sys.stderr)
        return 1
    print(f"unknown command '{cmd}'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
