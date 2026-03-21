# Angehlang Architecture Overview

## The "Universe OS" Philosophy
Angehlang is designed as more than just a programming language; it is a conceptual "Universe OS" (UOS). The language bridge-gaps between classical logic, human intent, and synthetic intelligence (AI).

### Key Pillars:
1.  **Entanglement**: Synchronized state across different environments.
2.  **Time Travel**: Native checkpointing and rewinding of execution state.
3.  **Swarm Intelligence**: Built-in primitives for multi-agent coordination.
4.  **Hardware Speculation**: Experimental photonic/quantum compilation targets.

## Project Structure

- `core/`: The heart of the language.
    - `interpreter.py`: The production-ready reference implementation. Highly flexible, supports all UOS features.
    - `integration_tests.angeh`: Comprehensive test suite for the interpreter.
    - `experimental/`: Speculative compilation targets (C transpiler, TS prototype).
- `stdlib/`: The standard library.
    - `core.angeh`: Basic predicates and list utilities.
    - `math.angeh`: Extended mathematical functions.
    - `string.angeh`: String manipulation.
    - `ai_bridge.angeh`: High-level AI swarm abstractions.
- `examples/`: Practical demonstrations of language features.
- `docs/`: In-depth guides for users and developers.

## Runtime Environment
The primary runtime is **Python 3.10+**. The interpreter uses a recursive-descent parser and an environment-based evaluator, allowing for rapid iteration and deep integration with Python's AI ecosystem (Ollama, PyTorch, etc.).
