#!/usr/bin/env bash
# ================================================================
# Angehlang Repository Reorganization Script
# Author contribution: Claude (Anthropic)
#
# Run from the root of the ace-lenz/Angehlang repository.
# Usage:  bash reorganize.sh [--dry-run]
#
# This script:
#  1. Creates the clean directory structure
#  2. Moves files to their correct locations
#  3. Deletes files confirmed safe to remove
#  4. Prints a summary
# ================================================================

set -euo pipefail

DRY_RUN=false
[[ "${1:-}" == "--dry-run" ]] && DRY_RUN=true

run() {
  if $DRY_RUN; then
    echo "[DRY] $*"
  else
    eval "$*"
  fi
}

info() { echo "  ➤  $*"; }
ok()   { echo "  ✅ $*"; }
skip() { echo "  ⏭  $*"; }

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Angehlang Repository Reorganizer                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# ── 1. Create directory structure ────────────────────────────────
info "Creating directory structure..."
for dir in \
  core stdlib lib visual tools bootstrap examples/advanced \
  examples/visual tests docs; do
  run "mkdir -p $dir"
done
ok "Directories ready"

# ── 2. Move core interpreter files ───────────────────────────────
info "Moving core files..."
for f in interpreter.py angehc.py angeh_runtime.h compiler.ts; do
  if [[ -f "$f" ]]; then
    run "git mv '$f' core/$f"
  elif [[ -f "core/$f" ]]; then
    skip "$f already in core/"
  fi
done

# Move self-hosting seeds if at root
for f in lexer.angeh parser.angeh angehlang.angeh; do
  if [[ -f "$f" && ! -f "core/$f" ]]; then
    run "git mv '$f' core/$f"
  fi
done
ok "Core files moved"

# ── 3. Move stdlib files ─────────────────────────────────────────
info "Moving stdlib files..."
for f in ai_bridge.angeh dotflow_a2a.angeh core.angeh math.angeh \
          memory.angeh collections.angeh string.angeh io.angeh \
          error_handler.angeh quantum.angeh; do
  if [[ -f "$f" && ! -f "stdlib/$f" ]]; then
    run "git mv '$f' stdlib/$f"
  elif [[ -f "stdlib/$f" ]]; then
    skip "$f already in stdlib/"
  fi
done
ok "Stdlib files moved"

# ── 4. Move example files ─────────────────────────────────────────
info "Moving example files..."
for f in 01_hello_world.angeh 02_fibonacci.angeh 03_ai_agents.angeh \
          04_swarm_roundtable.angeh; do
  if [[ -f "$f" && ! -f "examples/$f" ]]; then
    run "git mv '$f' examples/$f"
  fi
done

# Dataset files → examples/advanced
for f in *_dataset.angeh 4d_*.angeh 3d_*.angeh; do
  if [[ -f "$f" ]]; then
    run "git mv '$f' examples/advanced/$f"
  fi
done
ok "Examples moved"

# ── 5. Move visual/dotflow files ─────────────────────────────────
info "Moving visual files..."
for f in dotflow_core.angeh dotflow_compiler.angeh \
          parallel_dots_engine.angeh dotflow_renderer.angeh \
          dotflow_intelligence.angeh programming_dots.angeh \
          dot_quantization_table.angeh; do
  if [[ -f "$f" ]]; then
    TARGET="${f//_/-}"
    TARGET="${TARGET//dotflow-core/dotflow}"
    run "git mv '$f' visual/$TARGET"
  fi
done

# .dotflow files
for f in *.dotflow; do
  [[ -f "$f" ]] && run "git mv '$f' visual/$f"
done
ok "Visual files moved"

# ── 6. Move tool files ───────────────────────────────────────────
info "Moving tool files..."
for f in angeh_cli.angeh angehlang_lsp.angeh build_bootstrap.angeh; do
  if [[ -f "$f" && ! -f "tools/$f" ]]; then
    run "git mv '$f' tools/$f"
  fi
done
ok "Tool files moved"

# ── 7. Move doc files ────────────────────────────────────────────
info "Organizing documentation..."
for f in ARCHITECTURE.md CONTRIBUTING.md CODE_OF_CONDUCT.md \
          AI_GUIDE.md Synthetic_Intelligence_Spec.md CHANGELOG.md; do
  if [[ -f "$f" && ! -f "docs/$f" ]]; then
    run "git mv '$f' docs/$f"
  fi
done
# Keep README.md at root
ok "Docs organized"

# ── 8. DELETE: Log / temp / binary files ────────────────────────
info "Removing log/temp/binary files..."
for f in a2a_log.jsonl *.log error*.txt final*.txt \
          "logo.mp5" "logo.mp6" "download" \
          "Angehlang_Source_by_Longbian_Lennon.zip" \
          "Angehlang Logo.angeh" package-lock.angeh pyproject.angeh \
          requirements.angeh; do
  if [[ -f "$f" ]]; then
    run "git rm -f '$f'"
  fi
done
ok "Temp files removed"

# ── 9. DELETE: Redundant batch files ────────────────────────────
info "Removing emoji batch wrappers (keeping run.bat)..."
for f in "⚡.bat" "🏗️.bat" "🚀.bat" "📑.bat" "🧪.bat" "🧹.bat" "🏋️.bat" "📦.bat"; do
  if [[ -f "$f" ]]; then
    run "git rm -f '$f'"
  fi
done
ok "Emoji batch files removed"

# ── 10. DELETE: Confirmed obsolete Python files ──────────────────
info "Removing obsolete Python files (functionality merged to .angeh)..."
OBSOLETE_PY=(
  angeh_evolution.py angeh_neural.py angeh_photonic_3d.py
  angeh_reasoning.py angeh_neuron_storage.py emoji_3d_renderer.py
  emoji_compositor.py emoji_v17_engine.py engine.py enhanced_engine.py
  error_handler.py hardware_optimizer.py multi_modal_handler.py
  offline_bridge.py output_generators.py photonic_angeh_core.py
  photonic_execution_engine.py photonics_interpreter.py
  quantum_bridge.py realtime_parallel_execution.py
  universal_code_executor.py angeh_multimodal.py angeh_native_executor.py
)
for f in "${OBSOLETE_PY[@]}"; do
  if [[ -f "$f" ]]; then
    run "git rm -f '$f'"
  fi
done
ok "Obsolete Python files removed"

# ── 11. DELETE: VS Code stubs (superseded by angeh-lsp.angeh) ───
info "Removing VS Code stubs..."
for f in vscode_components.angeh vscode_main.angeh vscode_theme.angeh \
          ultimate_angeh_ide.angeh; do
  [[ -f "$f" ]] && run "git rm -f '$f'"
done
ok "VS Code stubs removed"

# ── 12. DELETE: 77D files (unclear purpose, no core logic) ──────
info "Removing 77D mystery files..."
for f in 77D_MASTER_KEY.angeh 77d.angeh 77d_dataset.angeh 77d_engine.angeh; do
  [[ -f "$f" ]] && run "git rm -f '$f'"
done
ok "77D files removed"

# ── 13. Rename runner PVM files ──────────────────────────────────
info "Removing unused PVM files..."
for f in runner.pvm shell.pvm substrate.pvm; do
  [[ -f "$f" ]] && run "git rm -f '$f'"
done
ok "PVM files removed"

# ── Summary ──────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Reorganization complete!                                ║"
echo "║                                                          ║"
echo "║  Next steps:                                             ║"
echo "║  1. Copy new files from the Claude contribution pack:    ║"
echo "║     core/{lexer,parser,evaluator,env}.angeh              ║"
echo "║     lib/{types,async,gc}.angeh                           ║"
echo "║     stdlib/collections.angeh                             ║"
echo "║     tools/{angeh-lsp,angeh-repl,angeh-pkg}.angeh         ║"
echo "║     docs/LANGUAGE.md                                     ║"
echo "║  2. git add -A                                           ║"
echo "║  3. git commit -m 'chore: reorganize + self-hosting v2'  ║"
echo "║  4. git push                                             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
