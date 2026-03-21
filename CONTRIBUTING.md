# Contributing to Angehlang

Welcome! Angehlang is a community-driven, AI-native programming language. Contributions of every kind are welcomed.

---

## 🚀 Quick Setup

1. **Clone the repo** and navigate to `Angehlang_standalone/`
2. Ensure you have **Python 3.10+** installed.
3. (Optional) Install [Ollama](https://ollama.ai) and run `ollama serve` for live AI features.
4. Launch the REPL: `python core/interpreter.py`

---

## 📁 Project Structure

| Path | Purpose |
|---|---|
| `core/interpreter.py` | The core Lisp/Angeh AST evaluator |
| `core/angehc.py` | C code transpiler (AOT backend) |
| `core/angeh_runtime.h` | C runtime header for native builds |
| `stdlib/*.angeh` | Standard library modules |
| `examples/*.angeh` | Beginner-friendly example programs |

---

## 🤝 How to Contribute

### Adding a Built-in Function
1. Add your Python function near the AI/Agent section in `interpreter.py`.
2. Register it in `create_global_env()` under a hyphenated Angehlang name.
3. Write a test expression in `core/dummy.angeh`.

### Adding a Standard Library Module
1. Create a new file: `stdlib/my-module.angeh`
2. Start the file with `(def-module my-module)`.
3. Define functions using `(def-fn ...)` or macros using `(def-macro ...)`.
4. Users can then include it with `(import my-module)`.

### Contribution Guidelines
- Keep `interpreter.py` focused on language core. Move domain logic to stdlib.
- Follow the existing S-expression style for `.angeh` files.
- Add a corresponding example to `examples/` when introducing a major feature.
- Update `CHANGELOG.md` under `[Unreleased]` with your change.

---

**Questions?** Open an issue! Created by Longbian Lennon.
