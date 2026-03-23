# ================================================================
# Angehlang Makefile
# Author contribution: Claude (Anthropic)
# ================================================================

PYTHON      := python3
ANGEH       := $(PYTHON) core/interpreter.py
ANGEHC      := $(PYTHON) core/angehc.py
CC          := gcc
CFLAGS      := -O2 -Wall -std=c11

.PHONY: all run repl test bootstrap install clean help

all: help

## Run a .angeh file:  make run FILE=examples/01_hello_world.angeh
run:
	@$(ANGEH) $(FILE)

## Start the interactive REPL
repl:
	@$(ANGEH) tools/angeh-repl.angeh

## Run all tests
test:
	@echo "Running test suite..."
	@for f in tests/*.angeh; do \
	  echo "  ▶ $$f"; \
	  $(ANGEH) $$f || exit 1; \
	done
	@echo "✅ All tests passed"

## Compile FILE to native binary:  make compile FILE=examples/02_fibonacci.angeh
compile:
	@$(ANGEHC) $(FILE)
	@$(CC) $(CFLAGS) -o $(basename $(FILE)) $(basename $(FILE)).c
	@echo "✅ Compiled: $(basename $(FILE))"

## Bootstrap self-hosting: run Stage 1 → 4
bootstrap:
	@echo "🚀 Stage 1: Lexer..."
	@$(ANGEH) core/lexer.angeh
	@echo "🚀 Stage 2: Parser..."
	@$(ANGEH) core/parser.angeh
	@echo "🚀 Stage 3: Evaluator..."
	@$(ANGEH) core/evaluator.angeh
	@echo "✅ Self-hosting complete"

## Start the LSP server
lsp:
	@$(ANGEH) tools/angeh-lsp.angeh

## Install a package:  make install PKG=mylib@1.0.0
install:
	@$(ANGEH) tools/angeh-pkg.angeh add $(PKG)

## Run hello world (smoke test)
hello:
	@$(ANGEH) examples/01_hello_world.angeh

## Clean compiled artifacts
clean:
	@find . -name "*.c" -not -path "*/core/*" -delete
	@find . -name "*.o" -delete
	@find . -name "*.exe" -delete
	@echo "🧹 Cleaned"

## Show this help
help:
	@echo ""
	@echo "  🌌 Angehlang Build System"
	@echo "  ─────────────────────────────────────────────────"
	@echo "  make run     FILE=<path>   Run a .angeh file"
	@echo "  make repl                  Start interactive REPL"
	@echo "  make test                  Run all tests"
	@echo "  make compile FILE=<path>   Compile to native binary"
	@echo "  make bootstrap             Test self-hosting stages"
	@echo "  make lsp                   Start LSP server"
	@echo "  make install PKG=name@ver  Install a package"
	@echo "  make clean                 Remove build artifacts"
	@echo "  ─────────────────────────────────────────────────"
	@echo ""
