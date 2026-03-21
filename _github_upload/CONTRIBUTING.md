# Contributing to Angehlang (Architectonic OS)

First off, thank you for considering contributing to the Angehlang ecosystem! We are building a truly self-hosted, distributed, and AI-native universal language.

## 🧱 Architectural Directives & Rules
Angehlang is an **Architectonic OS**. Code is treated as structural architecture.
1. **NO UNSAFE POINTERS**: The compiler physically enforces invariants banning the `'unsafe'` keyword natively. Do not submit code attempting to bypass base memory arrays.
2. **Immutable ASTs**: The native Parser guarantees that Nodes and Tokens cannot be mutated. Write purely functional cascades (`new-list`, `put!`).
3. **Decentralized Modularity**: Use `(import <name>)` cleanly dividing logic. Never build monolithic dependency towers.

## 🧪 Testing Your Contributions
We strictly enforce a deterministic True-Bootstrap pipeline. Before submitting Pull Requests, you MUST verify your structural edits do not randomly derive syntax evaluation output.
```bash
# Run the core validation mapping manually natively
python core/interpreter.py architectonic/test.angeh

# Run the strict Bootstrap verification matching A/B string outputs
python core/interpreter.py build_bootstrap.angeh
```
If `build_bootstrap.angeh` fails with `[SYSTEM FAILURE] Structural AST divergence!`, your PR will be automatically rejected.

## 📖 Submitting Pull Requests
- Keep PRs functionally distinct. 
- Ensure all native S-expressions utilize proper indentation.
- Document any new AI integration macros in `README.md`.
