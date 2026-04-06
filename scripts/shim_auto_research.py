#!/usr/bin/env python3
"""
Runtime shim to run the Angehlang auto_research skill.

This shim:
- Accepts CLI flags (--run-once, --dry-run, --query)
- Loads configuration (simple defaults here)
- Calls the Angehlang runtime (mocked here) to execute run_auto_research
- Persists the artifact JSON to artifact_path unless dry-run
"""  

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime

def load_config():
    # Minimal config mirroring the Angehlang defaults
    return {
        "enabled": True,
        "cadence": "daily",
        "sources": ["internal-knowledge-base"],
        "top_k": 3,
        "dry_run": False,
        "artifact_path": "artifacts/auto_research"
    }

def run_angehlang_skill_simulation(cfg, query):
    """
    Simulate calling the Angehlang skill. In a real integration this would call
    the runtime that can execute .angeh modules. For now we run the pure logic
    by re-implementing the expected interface.
    """
    # Lightweight deterministic artifact for testing
    plan = {
        "id": "sim-" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
        "name": "Simulated AutoResearch Plan",
        "steps": [f"Simulated step for query: {query}"],
        "provenance": ["simulated-finding-1"],
        "confidence": 0.75
    }
    artifact = json.dumps(plan, indent=2)
    return {
        "status": "ok",
        "artifact": artifact,
        "artifact_path": os.path.join(cfg["artifact_path"], plan["id"] + ".json"),
        "plan_id": plan["id"]
    }

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--run-once", action="store_true", help="Run a single execution")
    p.add_argument("--dry-run", action="store_true", help="Do not write artifacts")
    p.add_argument("--query", type=str, default="Angehlang: latest ideas")
    args = p.parse_args()

    cfg = load_config()
    cfg["dry_run"] = args.dry_run

    if not cfg["enabled"]:
        print("auto_research disabled in config", file=sys.stderr)
        sys.exit(0)

    if args.run_once:
        res = run_angehlang_skill_simulation(cfg, args.query)
        artifact = res["artifact"]
        path = res["artifact_path"]
        if cfg["dry_run"]:
            print("DRY RUN: would write artifact to", path)
            print(artifact)
            sys.exit(0)
        # persist
        ensure_dir(os.path.dirname(path))
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(artifact)
        print("Wrote artifact to", path)
        sys.exit(0)

    # In long-running mode we could loop on cadence. For safety, refuse here.
    print("No --run-once supplied; shim supports only single-run mode in this draft.", file=sys.stderr)
    sys.exit(2)

if __name__ == "__main__":
    main()