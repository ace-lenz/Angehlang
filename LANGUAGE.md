# Angehlang Language Specification

**Version:** 2.0  
**Author:** Longbian Lennon  
**Contributions:** Claude (Anthropic) — structural spec, formal grammar, standard library API  
**Status:** Living Document

---

## 1. Overview

Angehlang is a **homoiconic, AI-native, self-hosted** programming language. Its primary syntax is S-expressions (like Lisp/Scheme), enabling powerful macro systems and metaprogramming. The language is designed to be fully self-describing — every production tool (lexer, parser, evaluator, compiler, package manager, LSP) is written in `.angeh`.

### Design Principles

1. **Self-hosting first** — the language defines itself
2. **AI-native** — agents, LLMs, and multi-agent coordination are first-class primitives
3. **Persistent by default** — all collections are immutable; mutation is explicit with `!`
4. **Tail-call optimised** — deep recursion never blows the stack
5. **Typed gradually** — type annotations are optional; Hindley-Milner inference fills the gaps
6. **Visual + textual** — Dot Flow graphs and S-expressions are equivalent representations

---

## 2. Lexical Structure

### 2.1 Comments

```angeh
;; line comment — extends to end of line
```

Block comments are delimited by `#|` and `|#` (not yet in lexer v1, planned for v2.1).

### 2.2 Literals

| Kind    | Examples                          |
|---------|-----------------------------------|
| Integer | `0`, `42`, `-7`, `0xFF`, `0b1010` |
| Float   | `3.14`, `-0.5`, `1e10`, `1.5e-3`  |
| String  | `"hello"`, `"line\nnewline"`      |
| Char    | `#\a`, `#\space`, `#\newline`     |
| Bool    | `true`, `false`                   |
| Nil     | `nil`                             |
| Symbol  | `foo`, `x`, `my-var`, `+`, `<=`   |

### 2.3 Identifiers

A symbol may contain any character except whitespace, `(`, `)`, `"`, and `;`. Conventions:

- `kebab-case` — standard
- `predicate?` — returns bool
- `mutating!`  — modifies in place
- `CONSTANT`   — compile-time constant

---

## 3. Core Syntax (EBNF)

```ebnf
program     ::= form*
form        ::= atom | list
atom        ::= number | string | char | bool | nil | symbol
list        ::= '(' form* ')'
number      ::= integer | float
integer     ::= ['-'] digit+
float       ::= ['-'] digit+ '.' digit* [exponent]
exponent    ::= ('e' | 'E') ['+' | '-'] digit+
string      ::= '"' (char | escape)* '"'
escape      ::= '\' ('n' | 't' | 'r' | '\' | '"')
char        ::= '#\' char-name | '#\' any-char
bool        ::= 'true' | 'false'
nil         ::= 'nil'
symbol      ::= sym-char+
sym-char    ::= any char except whitespace | '(' | ')' | '"' | ';'
```

---

## 4. Special Forms

### 4.1 Binding

```angeh
(def name value)                    ; immutable binding
(set! name value)                   ; mutate existing binding
(def-fn name (params...) body...)   ; define function (sugar for def + lambda)
(def-macro name (params...) body...)
```

### 4.2 Control Flow

```angeh
(if test consequent alternate)
(cond (test body...)... (else body...))
(when test body...)
(unless test body...)
(and expr...)
(or expr...)
(not expr)
```

### 4.3 Binding Forms

```angeh
(let ((x v) ...) body...)           ; parallel binding
(let* ((x v) ...) body...)          ; sequential binding
(letrec ((x v) ...) body...)        ; recursive binding
```

### 4.4 Sequencing

```angeh
(begin expr...)                     ; evaluate in sequence, return last
(do ((var init step) ...)
    (test result)
    body...)                        ; C-style loop
```

### 4.5 Functions

```angeh
(lambda (params...) body...)        ; anonymous function
(lambda (a b . rest) body...)       ; variadic (rest collects extras)
```

### 4.6 Quoting & Macros

```angeh
(quote x)       ; equivalent: 'x — prevent evaluation
`(a ,b ,@c)     ; quasi-quote with unquote and splice
(macro-expand form)
```

### 4.7 Pattern Matching

```angeh
(match expr
  (pattern body...)
  ...)

;; Patterns:
;;  _              wildcard
;;  42, "str"      literal
;;  x              variable binding
;;  (a b c)        list destructuring
;;  (h . t)        head/tail
;;  'symbol        quoted symbol
```

### 4.8 Error Handling

```angeh
(try
  body
  (catch err handler)
  (finally cleanup))

(error "message")
(raise value)
```

### 4.9 Modules

```angeh
(def-module name "description")
(import module-name)
(export sym1 sym2 ...)
```

---

## 5. Type System

Angehlang uses Hindley-Milner inference. Types are inferred; annotations are optional.

### 5.1 Primitive Types

```
Int    Float    Num    Str    Bool    Char    Nil    Any    Never
```

### 5.2 Compound Types

```angeh
(List T)             ; homogeneous list
(Fn (A B) R)         ; function from A,B to R
(Tuple A B C)        ; fixed-length heterogeneous
(Record {x: Int})    ; named fields
(Union A B)          ; either A or B
```

### 5.3 Polymorphism

```angeh
(forall a. (Fn ((List a)) Int))   ; generic length
```

### 5.4 Type Annotations (optional)

```angeh
(def-fn square (x : Int) : Int
  (* x x))
```

---

## 6. Standard Library

### 6.1 `stdlib/core.angeh`
Fundamental list operations, boolean logic, I/O.

| Function          | Type signature                        |
|-------------------|---------------------------------------|
| `print`           | `Any → Nil`                           |
| `car`             | `(List a) → a`                        |
| `cdr`             | `(List a) → (List a)`                 |
| `cons`            | `a → (List a) → (List a)`            |
| `map`             | `(a→b) → (List a) → (List b)`        |
| `filter`          | `(a→Bool) → (List a) → (List a)`     |
| `reduce`          | `(b→a→b) → b → (List a) → b`        |
| `apply`           | `(Fn args r) → (List args) → r`      |

### 6.2 `stdlib/math.angeh`

| Function    | Description                    |
|-------------|--------------------------------|
| `+` `-` `*` `/` | Basic arithmetic          |
| `expt`      | Power                          |
| `sqrt`      | Square root                    |
| `log`       | Natural logarithm              |
| `sin/cos/tan` | Trigonometry                 |
| `floor/ceiling/round` | Rounding             |
| `gcd/lcm`   | Greatest common divisor / LCM  |
| `prime?`    | Primality test                 |
| `fib`       | Fibonacci (optimised)          |

### 6.3 `stdlib/collections.angeh`
Persistent Vector, Queue, Heap, Graph, Trie. See §7.

### 6.4 `stdlib/ai_bridge.angeh`

```angeh
(agent-spawn name system-prompt)
(agent-ask name prompt)
(agent-kill name)
(swarm-ask agent-list prompt)
(a2a-broadcast msg target-pattern bus)
(intend goal-description)
```

### 6.5 `stdlib/quantum.angeh`

```angeh
(qubit name)
(hadamard q)
(cnot control target)
(measure q)
(quantum-circuit name gates)
(simulate-circuit circuit shots)
```

---

## 7. Collections API Quick Reference

```angeh
;; Persistent Vector
(def v  (vec-new))
(def v2 (vec-conj v 42))         ; O(log N)
(vec-nth v2 0)                   ; → 42
(vec-count v2)                   ; → 1

;; Queue
(def q  (queue-new))
(def q2 (queue-enq q "hello"))
(queue-deq q2)                   ; → ("hello" . <empty-queue>)

;; Heap (priority queue)
(def h  (heap-min))
(def h2 (heap-push h 5))
(heap-peek (cadr (heap-pop h2))) ; → next element

;; Graph
(def g (graph-new))
(def g (graph-add-node g 'A "Node A"))
(def g (graph-add-edge g 'A 'B 1))
(graph-dijkstra g 'A)            ; → hash-map of distances

;; Trie
(def t (trie-new))
(def t (trie-insert t "hello" 42))
(trie-prefix-search t "hel")     ; → (("hello" 42))
```

---

## 8. Async / Concurrency API

```angeh
;; Green threads
(go (body))                       ; spawn coroutine
(sleep-ms 100)                    ; yield for 100ms

;; Channels
(def ch (make-channel 64))
(chan! ch "message")              ; send
(chan? ch)                        ; receive (blocks if empty)
(chan-close! ch)

;; Select (non-blocking multi-channel wait)
(select
  (list ch1 'recv (lambda (v) (print v)))
  (list ch2 'send "data" (lambda (_) nil)))

;; Promises
(def p (async (expensive-computation)))
(await p)

;; Actors
(def a (make-actor
  (lambda (state msg) (+ state msg))))
(actor-send! a 10)
```

---

## 9. AI Integration

```angeh
;; Spawn a named agent with a persona
(agent-spawn "Planner"
  "You are a strategic planning assistant.")

;; Ask the agent a question (non-blocking in async context)
(def plan (agent-ask "Planner" "Break down this task: build a compiler."))

;; Multi-agent swarm
(def agents (list "Planner" "Coder" "Critic"))
(swarm-ask agents "Improve this algorithm." plan)

;; Agent-to-Agent OmniBus
(a2a-broadcast "Task complete" "ALL" "MainBus")

;; Intent-driven programming (high-level)
(intend "sort this list by priority without mutation")
```

---

## 10. Visual / Dot Flow Programming

Angehlang programs can be represented as **Dot Graphs** — directed graphs where nodes are expressions and edges are data flows.

```angeh
(def-dotflow pipeline
  (→ (source input-file)
     (transform parse-csv)
     (map       validate-row)
     (filter    non-empty?)
     (reduce    aggregate-totals)
     (sink      output-json)))
```

Dot Flow programs compile to the same AST as textual S-expressions.

---

## 11. Self-Hosting Bootstrap Sequence

1. **Stage 0**: Substrate Python VM (`core/interpreter.py`) runs `core/lexer.angeh`
2. **Stage 1**: Native lexer tokenizes `core/parser.angeh`
3. **Stage 2**: Native parser parses `core/evaluator.angeh`
4. **Stage 3**: Native evaluator evaluates itself — full self-hosting achieved
5. **Stage 4**: Compiler (`tools/angehc.angeh`) compiles to native binary

---

## 12. Naming Conventions

| Pattern        | Meaning                               |
|----------------|---------------------------------------|
| `kebab-case`   | Functions and variables               |
| `UPPER-CASE`   | Module-level constants                |
| `Type-Case`    | Types (Int, List, Fn)                 |
| `name?`        | Predicate returning Bool              |
| `name!`        | Mutation (modifies in place)          |
| `name->other`  | Conversion (string->number)          |
| `*global*`     | Dynamic / special variables           |
| `__private__`  | Module-internal (not exported)        |

---

## 13. File Extensions

| Extension   | Description                              |
|-------------|------------------------------------------|
| `.angeh`    | Angehlang source file                    |
| `.angeh.d`  | Generated type declaration file          |
| `angeh.pkg` | Package manifest                         |
| `angeh.lock`| Dependency lock file                     |
| `.dotflow`  | Visual dot-graph source                  |

---

## 14. Changelog

- **v2.0** — Self-hosted lexer, parser, evaluator, type system, collections, LSP, REPL, package manager (all in `.angeh`)
- **v1.5** — Quantum stdlib, Dot Flow visual programming
- **v1.0** — Initial release with Python substrate VM

---

*"A language that can describe its own implementation has achieved true universality."*  
— Longbian Lennon
