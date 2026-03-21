# 🌌 Angehlang: The Universe OS
**Created by: Longbian Lennon**

Angehlang is a sentient, high-performance programming ecosystem designed for extreme computational workflows. Bridging the gap between high-level AI orchestration and bare-metal native execution, Angehlang is built to synthesize and govern the next generation of software architectures.

---

## 🚀 The Core Philosophy
Angehlang was engineered from the ground up to be **AI-Native**, **High-Performance**, and **Self-Evolving**. It acts not just as a syntax, but as a complete OS environment for your code.

- **AI-Native Intelligence**: Deep integration with Large Language Models directly within the AST using `(agent-spawn)`, `(agent-ask)`, and `(intend)` logic gates.
- **Agent-to-Agent (A2A) OmniBus**: A built-in massive telepathy protocol `(a2a-broadcast)` allowing autonomous agent swarms to communicate cross-process in real-time.
- **Polyglot Compilation Pipeline**: Angehlang natively parses resilient Abstract Syntax Trees and can execute them dynamically in Python, or transpile them to C Code with `angehc.py` for extreme raw performance.

---

## 🏗️ System Architecture

### 1. The Core Interpreter (`core/`)
The brain of Angehlang. A massively updated execution matrix featuring an extremely resilient regex-driven Lexer and memory-safe parsing engine.
- **`interpreter.py`**: The dynamic Python VM. Features a **colorized interactive REPL** with multi-line support and AI-assisted debugging.
- **`angehc.py` & `angeh_runtime.h`**: AOT (Ahead-of-Time) C transpilation backend.

### 2. The Standard Library (`stdlib/`)
- **`ai_bridge.angeh`**: Abstractions for Agent generation (`def-agent`, `swarm-gather`).
- **`dotflow_a2a.angeh`**: Routing for inter-process Agent communication (`a2a-announce`).
- **`core.angeh`, `math.angeh`, `string.angeh`**: Standard logic and math utilities.

### 3. The Dataset (`dataset/`)
Hundreds of theoretical modules ranging from 4D Quantization layers to Photonic Neural Networks, rigorously deduplicated and ready for research.

---

## 💻 Getting Started

### Prerequisites
Python 3.10+ is required. For AI features, a local LLM API (like Ollama on `localhost:11434`) is recommended.

### Launching the Environment
- **Windows**: Run **`run.bat`** for the interactive REPL.
- **Unix/macOS**: Run **`./run.sh`**.
- **REPL Commands**: Type `.help` inside the REPL for `.agents`, `.a2a`, and `.clear`.

### Running a Script
Execute `.angeh` files natively:
```bash
python core/interpreter.py examples/01_hello_world.angeh
```

---

## 🚀 Examples
Explore the **`examples/`** folder:
- `01_hello_world.angeh`: Basic syntax.
- `02_fibonacci.angeh`: Recursion.
- `03_ai_agents.angeh`: AI spawning.
- `04_swarm_roundtable.angeh`: A2A communication squads.

---

**License:** MIT  
**Author:** Longbian Lennon  
*Designed for the era of Sentient Computing.*
