---
name: dray-multiagent-linker
description: "Dray-inspired bi-directional multi-agent context bridge linking Google DeepMind Antigravity and OpenAI Codex (Desktop & Cloud sessions). Synchronizes shared memory, approved decisions, environment state, and file ownership locks across sessions without manual copy-pasting."
---

# 🔗 Dray Multi-Agent Linker (Antigravity ⟷ OpenAI Codex)

Inspired by the **Dray** multi-agent coordination paradigm:
> *"Claude, ChatGPT and Grok were built by rival companies, and none of them can read a word the others wrote. So you end up as the go-between, copying and pasting all day. Dray isn't another AI. It's how yours work together. Type `/link` in two chats and they read each other's messages."*

This skill bridges **Google DeepMind Antigravity** and **OpenAI Codex** into a unified, shared-memory pair-programming hivemind.

---

## ⚡ Multi-Model Fleet Architecture

Codex integrates multiple specialized models:

1. **`gpt-6.1-sol` (Flagship Pair Programmer)**:
   - Optimized for sub-second system code authoring, AST refactoring, script synthesis, and live debugging.
   - Primary driver for interactive code development and immediate implementation.
2. **`gpt-6-astra` (Frontier Deep Research & Security Sentinel)**:
   - Optimized for complex protocol verification, security audits, reverse engineering analysis, and formal proof verification.
   - Independent peer reviewer for architecture and critical system invariants.
3. **Multi-Model Parallel Consensus (`--multi`)**:
   - Dispatches prompts to both `gpt-6.1-sol` and `gpt-6-astra` concurrently, synthesizing multi-perspective hivemind consensus without sequential latency.

---

## 🛠️ Execution CLI

```bash
# Check Dray link health, verified models, and shared memory
python dray_codex_bridge.py status

# Synchronize current Antigravity context, state, and decisions into Dray Shared Memory
python dray_codex_bridge.py sync

# Query Codex models in parallel (gpt-6.1-sol + gpt-6-astra)
python dray_codex_bridge.py ask "<prompt>" --multi

# Query specifically the Flagship Pair Programmer
python dray_codex_bridge.py ask "<prompt>" --model gpt-6.1-sol

# Query specifically the Frontier Deep Research model
python dray_codex_bridge.py ask "<prompt>" --model gpt-6-astra

# Set a file ownership lock
python dray_codex_bridge.py lock "src/server/init.server.luau" --owner Antigravity

# Unlock a file
python dray_codex_bridge.py unlock "src/server/init.server.luau"
```

---

## 📌 Shared Memory Artifacts
- **Distilled Markdown Context**: `~/.codex/DRAY_SHARED_MEMORY.md`
- **Structured JSON State**: `~/.codex/DRAY_SHARED_MEMORY.json`
- **Latest Dual-Model Reply**: `~/.codex/CODEX_REPLY.md`
- **Coordination Audit Log**: `~/.codex/coordination_log.jsonl`

---

## 🔬 Protocol Invariants & Peer Review Lessons

1. **Dray Single-Owner File Partitioning**:
   - When Antigravity and OpenAI Codex collaborate on a complex project:
     - Each agent holds exclusive write locks over specific directory trees or files.
     - Never allow concurrent edits to the exact same file without explicit handoff.
     - Verified decisions and architectural schemas are permanently committed to `DRAY_SHARED_MEMORY.md`.

2. **IPC Channel Self-Recovery**:
   - If an internal container bridge encounters an `EBADF` (bad file descriptor) or pipe break during high-concurrency dispatch, the bridge falls back to filesystem-backed polling (`CODEX_REPLY.md`) to guarantee zero loss of consensus data.
