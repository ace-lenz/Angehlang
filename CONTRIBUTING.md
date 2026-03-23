# Contributing to Angehlang

Thank you for wanting to make Angehlang better! This guide explains the new self-hosting workflow introduced in v2.0.

---

## 🧱 Architecture Overview

```
angehlang/
├── core/          ← Self-hosting seeds (lexer, parser, evaluator, env)
├── stdlib/        ← Standard library (string, collections, io, ai_bridge…)
├── lib/           ← Advanced libraries (types, async, gc, net, crypto…)
├── visual/        ← Dot Flow visual programming engine
├── tools/         ← Developer tools (REPL, LSP, pkg manager, compiler)
├── bootstrap/     ← Minimal C runtime for Stage 0
├── examples/      ← Worked examples
│   └── advanced/  ← Dataset algorithms, benchmarks
├── tests/         ← Test suite (framework.angeh + test_all.angeh)
└── docs/          ← Documentation
```

### Self-Hosting Stages

| Stage | What runs what |
|-------|----------------|
| 0 | Python substrate (`core/interpreter.py`) executes everything |
| 1 | Native `core/lexer.angeh` tokenizes source |
| 2 | Native `core/parser.angeh` parses tokens |
| 3 | Native `core/evaluator.angeh` evaluates ASTs |
| 4 | `tools/angehc.angeh` compiles to native binary — **fully self-hosted** |

The goal of every contribution is to move more functionality from Stage 0 into Stages 1–4.

---

## 🚀 Getting Started

```bash
# Clone
git clone https://github.com/ace-lenz/Angehlang.git
cd Angehlang

# Run the REPL
make repl

# Run all tests
make test

# Run a single file
make run FILE=examples/01_hello_world.angeh
```

---

## 📝 Writing Angehlang Code

### The Golden Rules

1. **Write in `.angeh` first.** Only add Python/C when there is absolutely no way to implement a feature in Angehlang yet (e.g., syscalls, native I/O). Mark such functions `(native-fn ...)` and document them.

2. **Pure functions by default.** Use `!` suffix for anything that mutates state:
   ```angeh
   ;; Pure
   (def-fn vec-conj (v val) ...)
   ;; Mutating
   (def-fn env-define! (env sym val) ...)
   ```

3. **Export explicitly.** Every module must end with `(export ...)`.

4. **Document with docstrings.** The second argument to `def-fn` or `def-module` is the docstring:
   ```angeh
   (def-fn my-fn (x)
     "Compute the square of x."
     (* x x))
   ```

5. **Write tests.** Use `tests/framework.angeh`. See `tests/test_all.angeh` for examples.

---

## 🗂 Where to Put New Code

| What you're adding | Where it goes |
|--------------------|---------------|
| Language core change (new special form, evaluator fix) | `core/evaluator.angeh` |
| New type system feature | `lib/types.angeh` |
| New collection (e.g., B-tree) | `stdlib/collections.angeh` |
| New I/O format (e.g., TOML parser) | `stdlib/io.angeh` |
| New async primitive | `lib/async.angeh` |
| New visual/dotflow feature | `visual/` |
| New tool (linter, formatter) | `tools/` |
| New worked example | `examples/` |
| New advanced algorithm | `examples/advanced/` |
| Tests for the above | `tests/` |

---

## ✅ Checklist Before Opening a PR

- [ ] Code is written in `.angeh` (not Python/C) wherever possible
- [ ] New functions are exported from their module
- [ ] Docstrings are present
- [ ] Tests written in `tests/` and passing (`make test`)
- [ ] `make bootstrap` succeeds (self-hosting stages not broken)
- [ ] No emoji-named files (use descriptive names)
- [ ] No `*_dataset.angeh` at root — datasets go in `examples/advanced/`
- [ ] No temp/log files committed

---

## 🐛 Reporting Bugs

Open an issue with:
- Angehlang version
- Minimal reproduction (`.angeh` snippet)
- Expected vs actual output

---

## 🌟 Ideas for Contributions

- **Type system**: add record types, union exhaustiveness checking
- **Collections**: B-tree, skip list, bloom filter
- **Async**: work-stealing scheduler, select with timeout
- **String**: full Unicode normalization (NFC/NFD)
- **Tools**: code formatter (`angeh-fmt.angeh`), linter (`angeh-lint.angeh`)
- **Visual**: Dot Flow → SVG renderer
- **Examples**: more AI agent patterns, quantum circuit demos

---

*Written with ❤️ by Longbian Lennon 
+Google
+Deepseek
+Ollama
+Claude (Anthropic)*
