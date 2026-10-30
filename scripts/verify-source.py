"""Check that the vendored kernel and bridge match the reviewed lock."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
lock = json.loads((ROOT / "build-lock.json").read_text())
expected = json.loads((ROOT / "core/kernel-files.json").read_text())
folder = ROOT / "core/Clash.Meta"
actual = {str(p.relative_to(folder)).replace("\\", "/"): hashlib.sha256(p.read_bytes()).hexdigest()
          for p in sorted(folder.rglob("*")) if p.is_file() and not any(x in p.relative_to(folder).parts for x in (".git", "dist", ".toolchain"))}
if actual != expected:
    changes = sorted(k for k in actual.keys() | expected.keys() if actual.get(k) != expected.get(k))
    raise SystemExit("Kernel differs from build lock: " + ", ".join(changes))
patch = ROOT / lock["kernel"]["bridge_patch"]
if hashlib.sha256(patch.read_bytes()).hexdigest() != lock["kernel"]["bridge_sha256"]:
    raise SystemExit("Bridge patch differs from build lock")
print("Kernel source verified:", lock["kernel"]["commit"])
