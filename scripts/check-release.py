"""Release only a successful package run with matching device acceptance evidence."""
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
run_id, tag = sys.argv[1:3]
if not run_id.isdecimal() or not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+-plus\.[0-9]+", tag):
    raise SystemExit("Invalid run ID or prerelease tag (expected vX.Y.Z-plus.N)")
repo = "jack4pear/bettboxPlus"
run = json.loads(subprocess.check_output(["gh", "api", f"repos/{repo}/actions/runs/{run_id}"], text=True))
if run["conclusion"] != "success" or run["path"] != ".github/workflows/build.yaml":
    raise SystemExit("Release blocked: package workflow must finish successfully")
acceptance = json.loads((root / "docs/ACCEPTANCE.json").read_text())
if acceptance["source_commit"] != run["head_sha"]:
    raise SystemExit("Release blocked: device acceptance must name the packaged source commit")
for target in ("windows_x64", "android_arm64"):
    record = acceptance[target]
    if record["status"] != "passed" or not record["evidence"].strip():
        raise SystemExit("Release blocked: missing physical-device acceptance for " + target)
subprocess.run(["git", "diff", "--exit-code", run["head_sha"], "HEAD", "--", ".", ":!docs/ACCEPTANCE.json", ":!docs/ACCEPTANCE.md"], cwd=root, check=True)
lock = json.loads((root / "build-lock.json").read_text())
expected_tag = "v" + lock["client"]["version"].split("+")[0]
if tag != expected_tag:
    raise SystemExit("Release tag must match build-lock.json: " + expected_tag)
print("Acceptance and package source verified:", run["head_sha"])
