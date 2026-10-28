# Dray Multi-Agent Linker Directives

When this plugin/integration is active:
1. **Shared Context**: Dray shared memory is synchronized at `~/.codex/DRAY_SHARED_MEMORY.md` and `.json`.
2. **Zero Copy-Paste Mandate**: Query Codex directly via `python dray_codex_bridge.py ask "<prompt>"`.
3. **File Ownership Locks**: Keep one owner per edited file; share evidence and material decisions before modifying locked paths.
4. **Permanent Decision Ledger**: Record approved architectural decisions in the shared memory so both agents respect them across turns.
