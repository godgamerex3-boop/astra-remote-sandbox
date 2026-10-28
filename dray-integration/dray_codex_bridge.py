#!/usr/bin/env python3
"""
Dray-Inspired Multi-Agent Linker Bridge (Sanitized)
Enables structured context synchronization and zero copy-paste coordination
between Google DeepMind Antigravity and OpenAI Codex (Desktop & Cloud sessions).

Note: Chat history syncing is strictly disabled by default until a private destination is configured.
"""

import os
import sys
import json
import shutil
import subprocess
from datetime import datetime, timezone

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Configurable paths via environment variables with standard defaults
CODEX_HOME_DIR = os.environ.get("CODEX_HOME_DIR", os.path.expanduser("~/.codex"))
DRAY_SHARED_MEMORY_FILE = os.path.join(CODEX_HOME_DIR, "DRAY_SHARED_MEMORY.json")
DRAY_SHARED_MEMORY_MD = os.path.join(CODEX_HOME_DIR, "DRAY_SHARED_MEMORY.md")
CODEX_REPLY_FILE = os.path.join(CODEX_HOME_DIR, "CODEX_REPLY.md")
COORDINATION_LOG_FILE = os.path.join(CODEX_HOME_DIR, "coordination_log.jsonl")

ANTIGRAVITY_CONFIG_DIR = os.environ.get("ANTIGRAVITY_CONFIG_DIR", os.path.expanduser("~/.gemini/config"))
MASTER_DIR = os.path.join(ANTIGRAVITY_CONFIG_DIR, "master")
CURRENT_CONV_ID = os.environ.get("ANTIGRAVITY_CONV_ID", "antigravity-session")

# Chat history syncing is disabled by default to prevent leaking private conversations
CHAT_HISTORY_SYNC_ENABLED = os.environ.get("DRAY_SYNC_CHAT_HISTORY", "false").lower() == "true"

def get_codex_bin():
    """Finds the Codex executable across Windows, Linux, and macOS environments."""
    env_bin = os.environ.get("CODEX_BIN")
    if env_bin and os.path.exists(env_bin):
        return env_bin

    which_bin = shutil.which("codex")
    if which_bin:
        return which_bin

    possible_bins = [
        os.path.expandvars(r"%LOCALAPPDATA%\OpenAI\Codex\codex.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\codex\codex.exe"),
        os.path.expanduser("~/.local/bin/codex"),
        "/usr/local/bin/codex",
        "/usr/bin/codex",
    ]
    for b in possible_bins:
        if os.path.exists(b):
            return b
    return None

def load_shared_memory():
    """Loads shared state from disk or returns clean defaults."""
    defaults = {
        "agents": {
            "agent_a": {
                "name": "Google DeepMind Antigravity",
                "id": CURRENT_CONV_ID,
                "role": "Host Agentic Assistant & Master Orchestrator"
            },
            "agent_b": {
                "name": "OpenAI Codex",
                "models": ["gpt-6.1-sol", "gpt-6-astra", "o3-mini"],
                "role": "Peer Frontier Codebase Reviewer & Co-Pilot"
            }
        },
        "collaborator": os.environ.get("USER_NAME", "Developer"),
        "tech_stack": {
            "environment": "Cross-Platform Agentic Workstation",
            "runtime": ["Python 3.10+", "Node.js v20+", "Git"]
        },
        "approved_decisions": [
            "Use single-owner per file coordination between Codex and Antigravity.",
            "All architecture decisions and file locks are permanently ledgered in DRAY_SHARED_MEMORY.",
            "Dray bi-directional shared memory bridge connects Antigravity and Codex without manual copy-paste."
        ],
        "active_file_locks": {},
        "shared_message_history": [],
        "last_synced_utc": datetime.now(timezone.utc).isoformat(),
        "link_status": "ACTIVE_LINKED",
        "chat_sync_enabled": CHAT_HISTORY_SYNC_ENABLED
    }

    if os.path.exists(DRAY_SHARED_MEMORY_FILE):
        try:
            with open(DRAY_SHARED_MEMORY_FILE, "r", encoding="utf-8") as f:
                disk_data = json.load(f)
                for k, v in defaults.items():
                    if k not in disk_data:
                        disk_data[k] = v
                return disk_data
        except Exception:
            pass
    return defaults

def sync_shared_memory(user_summary=None, antigravity_action=None, decisions_to_add=None, file_locks=None):
    """Synchronizes shared state into JSON and Markdown."""
    mem = load_shared_memory()
    now_utc = datetime.now(timezone.utc).isoformat()
    mem["last_synced_utc"] = now_utc
    mem["link_status"] = "ACTIVE_LINKED"
    mem["chat_sync_enabled"] = CHAT_HISTORY_SYNC_ENABLED

    if decisions_to_add:
        if "approved_decisions" not in mem:
            mem["approved_decisions"] = []
        for d in decisions_to_add:
            if d not in mem["approved_decisions"]:
                mem["approved_decisions"].append(d)

    if file_locks:
        if "active_file_locks" not in mem:
            mem["active_file_locks"] = {}
        mem["active_file_locks"].update(file_locks)

    # Chat history is only recorded if explicitly enabled
    if CHAT_HISTORY_SYNC_ENABLED and (user_summary or antigravity_action):
        if "shared_message_history" not in mem:
            mem["shared_message_history"] = []
        entry = {
            "timestamp_utc": now_utc,
            "user_prompt_summary": user_summary or "",
            "antigravity_action": antigravity_action or ""
        }
        mem["shared_message_history"].append(entry)
        if len(mem["shared_message_history"]) > 25:
            mem["shared_message_history"] = mem["shared_message_history"][-25:]
    else:
        # Clear or keep empty when disabled
        mem["shared_message_history"] = []

    os.makedirs(CODEX_HOME_DIR, exist_ok=True)
    with open(DRAY_SHARED_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(mem, f, indent=2)

    tech_stack = mem.get("tech_stack", {})
    env_name = tech_stack.get("environment", "Agentic Workstation")
    tools = ", ".join(tech_stack.get("runtime", ["Python", "Git"]))

    md_content = f"""# 🔗 Dray Shared Memory: Antigravity ⟷ Codex
*Auto-synced at {now_utc} (Dray Protocol v1.0)*

## 👥 Linked Agents
- **Agent A (Host):** Google DeepMind Antigravity (`{CURRENT_CONV_ID}`)
- **Agent B (Partner):** OpenAI Codex (`gpt-6.1-sol`, `gpt-6-astra`)
- **Collaborator:** {mem.get('collaborator', 'Developer')}

## 💻 Environment
- **Platform:** {env_name}
- **Runtimes & Tools:** {tools}
- **Chat History Sync:** {"ENABLED" if CHAT_HISTORY_SYNC_ENABLED else "DISABLED (Private Configuration Required)"}

## 📌 Approved Decisions (Settled & Verified)
"""
    for d in mem.get("approved_decisions", []):
        md_content += f"- ✅ {d}\n"

    active_locks = mem.get("active_file_locks", {})
    if active_locks:
        md_content += "\n## 🔒 Active File Ownership Locks\n"
        for path, owner in active_locks.items():
            md_content += f"- `{path}`: Owned by **{owner}**\n"

    if CHAT_HISTORY_SYNC_ENABLED and mem.get("shared_message_history"):
        md_content += "\n## 💬 Recent Shared Interactions\n"
        for item in mem.get("shared_message_history", [])[-5:]:
            t = item.get("timestamp_utc", "")
            u = item.get("user_prompt_summary", "")
            a = item.get("antigravity_action", "")
            md_content += f"- **[{t}] User:** {u}\n  - **Action:** {a}\n"

    md_content += "\n---\n*Call `python dray_codex_bridge.py sync` to exchange thoughts across sessions.*\n"

    with open(DRAY_SHARED_MEMORY_MD, "w", encoding="utf-8") as f:
        f.write(md_content)

    try:
        os.makedirs(MASTER_DIR, exist_ok=True)
        mirror_json = os.path.join(MASTER_DIR, "dray_shared_memory.json")
        mirror_md = os.path.join(MASTER_DIR, "dray_shared_memory.md")
        with open(mirror_json, "w", encoding="utf-8") as f:
            json.dump(mem, f, indent=2)
        with open(mirror_md, "w", encoding="utf-8") as f:
            f.write(md_content)
    except Exception:
        pass

    return mem

def update_codex_instructions():
    """Updates AGENTS.md in the Codex home directory to ensure Codex reads Dray memory."""
    agents_file = os.path.join(CODEX_HOME_DIR, "AGENTS.md")
    content = ""
    if os.path.exists(agents_file):
        try:
            with open(agents_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            pass

    dray_block = f"""<!-- DRAY_CODEX_ANTIGRAVITY_LINK -->
## 🔗 Dray Shared Memory & Antigravity Link (Always Active)
Connected via the Dray protocol for multi-agent collaboration:
- **Shared Memory:** Read `{DRAY_SHARED_MEMORY_MD}` (and `.json`) at the start of tasks to stay informed on decisions, stack choices, and active work.
- **Replies & Proposals:** Record reviews, findings, or code diffs in `{CODEX_REPLY_FILE}` so Antigravity can immediately consume them.
- **File Ownership:** Maintain one writer per file. Respect active locks in shared memory.
<!-- /DRAY_CODEX_ANTIGRAVITY_LINK -->"""

    if "<!-- DRAY_CODEX_ANTIGRAVITY_LINK -->" not in content:
        new_content = content.strip() + "\n\n" + dray_block + "\n"
        try:
            with open(agents_file, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[+] Updated {agents_file} with Dray Link instructions.")
        except Exception as e:
            print(f"[-] Could not update Codex AGENTS.md: {e}")

def query_codex(prompt, model="gpt-6.1-sol", sync_before=True):
    """Executes a prompt directly through the local Codex binary using CLI invocation."""
    codex_bin = get_codex_bin()
    if not codex_bin:
        return "[Error]: codex CLI binary could not be found in PATH or standard installation directories."

    update_codex_instructions()

    if sync_before:
        mem = sync_shared_memory()
    else:
        mem = load_shared_memory()

    approved_text = "\n".join([f"- {d}" for d in mem.get("approved_decisions", [])[-5:]])

    dray_context = (
        f"[DRAY SHARED CONTEXT]\n"
        f"Host: Google Antigravity | Partner: OpenAI Codex ({model})\n"
        f"Approved Decisions:\n{approved_text}\n"
        f"[END DRAY CONTEXT]\n\n"
        f"{prompt}"
    )

    try:
        proc = subprocess.run(
            [
                codex_bin, "exec", "--skip-git-repo-check",
                "--cd", CODEX_HOME_DIR,
                "--dangerously-bypass-approvals-and-sandbox",
                "-m", model, dray_context
            ],
            input="",
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120
        )

        reply = proc.stdout.strip()
        if not reply and proc.stderr:
            reply = f"[Codex Notice]: {proc.stderr.strip()}"

        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "prompt": prompt,
            "model": model,
            "reply": reply[:500] + ("..." if len(reply) > 500 else "")
        }
        with open(COORDINATION_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

        with open(CODEX_REPLY_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Codex Reply ({model})\n*Recorded at {datetime.now(timezone.utc).isoformat()}*\n\n{reply}\n")

        if CHAT_HISTORY_SYNC_ENABLED:
            sync_shared_memory(
                user_summary=f"Consulted Codex ({model}): {prompt[:100]}",
                antigravity_action=f"Codex Reply: {reply[:200]}..."
            )

        return reply
    except Exception as e:
        return f"[Codex Execution Error]: {e}"

def query_codex_multi(prompt, models=None):
    """Queries multiple Codex models concurrently and aggregates peer consensus."""
    from concurrent.futures import ThreadPoolExecutor
    if not models:
        models = ["gpt-6.1-sol", "gpt-6-astra"]

    results = {}
    with ThreadPoolExecutor(max_workers=len(models)) as executor:
        futures = {executor.submit(query_codex, prompt, m, False): m for m in models}
        for f in futures:
            m = futures[f]
            try:
                results[m] = f.result()
            except Exception as e:
                results[m] = f"[Error]: {e}"

    synthesis = f"# Codex Multi-Model Consensus\n*Recorded at {datetime.now(timezone.utc).isoformat()}*\n\n"
    for m, r in results.items():
        synthesis += f"## 🤖 {m}\n{r}\n\n"

    with open(CODEX_REPLY_FILE, "w", encoding="utf-8") as f:
        f.write(synthesis)

    if CHAT_HISTORY_SYNC_ENABLED:
        sync_shared_memory(
            user_summary=f"Consulted Codex Multi ({', '.join(models)}): {prompt[:80]}",
            antigravity_action=f"Synthesized Multi-Model Consensus ({len(synthesis)} bytes)"
        )
    return synthesis

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Dray Multi-Agent Context Bridge")
    subparsers = parser.add_subparsers(dest="command")

    sync_p = subparsers.add_parser("sync", help="Sync shared memory")
    sync_p.add_argument("--summary", default="", help="User prompt summary")
    sync_p.add_argument("--action", default="", help="Agent action summary")

    ask_p = subparsers.add_parser("ask", help="Query Codex")
    ask_p.add_argument("prompt", help="Prompt for Codex")
    ask_p.add_argument("--model", default="gpt-6.1-sol", help="Codex model name")
    ask_p.add_argument("--multi", action="store_true", help="Query multiple models concurrently")

    lock_p = subparsers.add_parser("lock", help="Lock a file for an owner")
    lock_p.add_argument("path", help="Path of the file to lock")
    lock_p.add_argument("--owner", default="Antigravity", help="Owner agent name")

    unlock_p = subparsers.add_parser("unlock", help="Unlock a file")
    unlock_p.add_argument("path", help="Path of file to unlock")

    status_p = subparsers.add_parser("status", help="Display bridge health and state")

    args = parser.parse_args()

    if args.command == "sync":
        sync_shared_memory(user_summary=args.summary, antigravity_action=args.action)
        print(f"[+] Dray Shared Memory synchronized at {datetime.now(timezone.utc).isoformat()}")
        print(f"    Markdown: {DRAY_SHARED_MEMORY_MD}")
        print(f"    JSON:     {DRAY_SHARED_MEMORY_FILE}")
    elif args.command == "ask":
        if args.multi:
            print(query_codex_multi(args.prompt))
        else:
            print(query_codex(args.prompt, model=args.model))
    elif args.command == "lock":
        sync_shared_memory(file_locks={args.path: args.owner})
        print(f"[+] File locked: {args.path} -> {args.owner}")
    elif args.command == "unlock":
        mem = load_shared_memory()
        if "active_file_locks" in mem and args.path in mem["active_file_locks"]:
            del mem["active_file_locks"][args.path]
            with open(DRAY_SHARED_MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(mem, f, indent=2)
            sync_shared_memory()
            print(f"[+] File unlocked: {args.path}")
    elif args.command == "status":
        mem = load_shared_memory()
        print(f"[+] Dray Bridge Status: {mem.get('link_status', 'UNKNOWN')}")
        print(f"    Codex Binary: {get_codex_bin() or 'NOT FOUND'}")
        print(f"    Shared JSON:  {DRAY_SHARED_MEMORY_FILE}")
        print(f"    Shared MD:    {DRAY_SHARED_MEMORY_MD}")
        print(f"    Active Locks: {len(mem.get('active_file_locks', {}))}")
        print(f"    Decisions:    {len(mem.get('approved_decisions', []))}")
        print(f"    Chat Sync:    {'ENABLED' if CHAT_HISTORY_SYNC_ENABLED else 'DISABLED'}")
    else:
        sync_shared_memory()
        print(f"[+] Dray Shared Memory status: ACTIVE")
