# Angehlang AI Integration Guide

Angehlang is uniquely designed to be "AI-First." It provides native primitives for spawning, querying, and orchestrating Large Language Models (LLMs).

## Setting Up Providers
Angehlang's interpreter (`core/interpreter.py`) automatically attempts to connect to local AI providers in the following order:
1.  **Ollama**: `http://localhost:11434` (Default model: `llama3`)
2.  **LMStudio**: `http://localhost:1234` (OpenAI-compatible local server)

Ensure one of these is running to enable live AI features.

## Core AI Primitives

### 1. Spawning Agents
Use `(agent-spawn name system-prompt)` to create a new agent.
```scheme
(agent-spawn "Oracle" "You are a wise advisor who speaks in riddles.")
```

### 2. Querying Agents
Use `(agent-ask name prompt)` to get a response. Conversation history is managed automatically.
```scheme
(def-fn solve-riddle (q)
  (agent-ask "Oracle" q))
```

### 3. Swarm Intelligence (A2A)
Agents can communicate with each other using the "Agent-to-Agent" (A2A) protocol.
```scheme
(a2a-broadcast "Attention all agents: The simulation has begun.")
```

## AI-Driven Auto-Correction
The Angehlang REPL includes a self-healing mechanism. If an expression leads to an error, the interpreter can optionally query a hidden `__ERROR_HELPER__` agent to suggest a fix.

## Best Practices for LLM Users
When asking an AI to write Angehlang code:
- Tell it it is an **S-expression based language** similar to Clojure or Scheme.
- Mention the **UOS Features** like `entangle` and `checkpoint`.
- Provide the output of `(help)` as context for available built-ins.
