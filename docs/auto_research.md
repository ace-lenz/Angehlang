# Auto Research Skill (auto_research)

Overview
--------
The `auto_research` skill automates lightweight discovery, evaluation, and plan synthesis.
It is intentionally divided between pure logic (in Angehlang) and a small runtime shim (Python)
which handles side-effects like network access and filesystem persistence.

Why this design?
- Pure logic in Angehlang: deterministic, testable, and safe for static analysis.
- Shim in Python: integrates with existing tools, can be run in CI or on a server, and performs network/file I/O.

Files added
- `skills/auto_research.angeh` — core skill logic, pure functions + a single entrypoint `run_auto_research`.
- `scripts/shim_auto_research.py` — small CLI that calls the skill, persists artifacts, and supports dry-run.
- `tests/test_auto_research.py` — unit tests that verify the shim and the skill interop without external network.

Usage
1. Review/adjust configuration in your Angehlang runtime:
   - cadence, sources, top_k, artifact_path
2. Run the shim for a single execution:
   - `python3 scripts/shim_auto_research.py --run-once --query "quantum storage review" --dry-run`
3. Configure scheduler (systemd/cron/CI) to run on the configured cadence.

Extending the skill
- Replace the `discover` placeholders with runtime-side network fetches via the shim.
- Add domain-specific scoring in `evaluate`.
- Implement action handlers that can open issues, create drafts, or schedule experiments.

Security & Privacy
- The core Angehlang code is pure and contains no secrets.
- The shim is responsible for handling credentials (e.g., tokens) — it should read them from secure environment variables or vaults.

Contribution notes
- Keep heavy I/O out of `.angeh` modules to maintain testability.
- Add integration tests for new sources in `tests/` and mock network calls in the shim.
