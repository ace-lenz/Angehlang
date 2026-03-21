# Angehlang Changelog

All notable changes to this project are documented here.

---

## [v2.1.0] — 2026-03-21
**Author: Longbian Lennon**

### ✨ New Features
- **Interactive REPL**: Run `python core/interpreter.py` for a live session with colorized prompt, `.help`, `.agents`, `.a2a`, `.clear`, `.exit` dot commands and multi-line expression support.
- **Real `(import)` System**: `(import ai-bridge)`, `(import dotflow-a2a)` now actually load and evaluate stdlib files at runtime.
- **AI Auto-Correction**: Syntax errors display in red/yellow with a 💡 AI suggestion when Ollama is available.
- **`(reflect)`**: Dynamic environment introspection for AI/SI agents — inspect all globals, agents, and A2A packets as JSON.
- **`(version)` & `(help)`**: Built-in language query functions.
- **4 New Agent APIs**: `agent-forget`, `agent-recall`, `agent-list`, `agent-clone`.
- **Multi-Provider AI Routing**: Auto-rotates through Ollama → LM Studio → Mock fallback.
- **Full Conversation History**: `agent-ask` now sends the last 20 turns as context.
- **Persistent A2A Log**: All A2A broadcast packets are appended to `a2a_log.jsonl` on disk.
- **`examples/` Folder**: 4 ready-to-run example programs (hello world, fibonacci, agents, swarm).
- **Launcher Scripts**: `run.bat` (Windows) & `run.sh` (Unix) for one-click startup.

### 🔧 Bug Fixes
- Fixed `Unexpected ')'` syntax error caused by naive string splitting in the tokenizer (replaced with `re.findall` regex engine).
- Fixed `cond` form to support multi-expression clause bodies.
- Fixed `Symbol` type to properly distinguish variables from string literals.
- Fixed `prune.py` auto-audit removal of 194 duplicated dataset files.

---

## [v2.0.0] — 2026-03-20

### ✨ New Features
- Native AI agent spawning (`agent-spawn`, `agent-ask`).
- Agent-to-Agent (A2A) OmniBus broadcast system.
- `intend` function for natural-language intent resolution.
- `ai_bridge.angeh` and `dotflow_a2a.angeh` standard library modules.
- C transpilation backend (`angehc.py`, `angeh_runtime.h`).

---

## [v1.0.0] — Legacy

- Initial Angehlang interpreter with Lisp-like S-expression syntax.
- Basic arithmetic, conditionals, loops, lambdas, and closures.
- DotFlow photonic pipeline (conceptual dataset).
- VM architecture and compiler pipeline prototype.
