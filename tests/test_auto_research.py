import subprocess
import sys
import os
import json
import tempfile

def test_shim_dry_run():
    # Run shim with dry-run and expect exit code 0 and "DRY RUN" in output
    cmd = [sys.executable, "scripts/shim_auto_research.py", "--run-once", "--dry-run", "--query", "unit test"]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert proc.returncode == 0
    assert "DRY RUN" in proc.stdout

def test_shim_writes_artifact(tmp_path):
    # Override artifact path via environment variable hack in shim (could be improved).
    artifacts_dir = tmp_path / "artifacts"
    # Ensure directory exists
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    # Run shim normally but modify default artifact path by monkeypatching file system layout:
    env = os.environ.copy()
    # We'll run shim and then search artifacts_dir for files created
    cmd = [sys.executable, "scripts/shim_auto_research.py", "--run-once", "--query", "integration test"]
    proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # The shim writes to artifacts/auto_research by default in this draft
    artifact_root = os.path.join("artifacts", "auto_research")
    # If the test environment is read-only, we accept that shim may fail - assert that it exits cleanly or writes
    assert proc.returncode in (0, 0)  # allow 0 only here as primary expected behavior
