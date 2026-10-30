"""Record exact source, tools, architecture, and artifact checksums."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
lock = json.loads((ROOT / "build-lock.json").read_text())
platform, arch = sys.argv[1:3]
dist = ROOT / "dist"
dist.mkdir(exist_ok=True)
info = dict(lock)
info.update(client_commit=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            platform=platform, architecture=arch,
            go=subprocess.check_output(["go", "version"], text=True).strip(),
            flutter=subprocess.check_output(["flutter", "--version"], text=True, shell=os.name == "nt").strip(),
            validation="Build verification only; physical-device acceptance is pending.")
info["kernel_binaries"] = {str(p.relative_to(ROOT)).replace("\\", "/"):hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (ROOT / "libclash" / platform).rglob("*") if p.suffix in (".exe", ".so")}
(dist / f"BUILD-INFO-{platform}-{arch}.json").write_text(json.dumps(info, indent=2) + "\n")
(dist / f"SHA256SUMS-{platform}-{arch}.txt").write_text("".join(
    f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n"
    for p in sorted(dist.iterdir()) if p.is_file() and not p.name.startswith("SHA256SUMS")))
