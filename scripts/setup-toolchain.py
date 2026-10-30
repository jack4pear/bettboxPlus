"""Install the checksum-pinned MetaCubeX Go toolchain (not stock Go)."""
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import tarfile
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
lock = json.loads((ROOT / "build-lock.json").read_text())["toolchain"]
system = platform.system().lower()
arch = {"x86_64": "amd64", "AMD64": "amd64", "aarch64": "arm64", "ARM64": "arm64"}[platform.machine()]
asset = lock["archives"][f"{system}-{arch}"]
folder = ROOT / ".toolchain"
folder.mkdir(exist_ok=True)
archive = folder / asset["file"]
if not archive.exists() or hashlib.sha256(archive.read_bytes()).hexdigest() != asset["sha256"]:
    urllib.request.urlretrieve(lock["base_url"] + asset["file"], archive)
if hashlib.sha256(archive.read_bytes()).hexdigest() != asset["sha256"]:
    raise SystemExit("MetaCubeX Go checksum mismatch; refusing extraction")
# Extract every run: a pre-existing stock Go executable must never bypass the pin.
if archive.suffix == ".zip":
    with zipfile.ZipFile(archive) as package:
        package.extractall(folder)
else:
    with tarfile.open(archive) as package:
        package.extractall(folder, filter="data")
go_bin = folder / "go" / "bin"
version = subprocess.check_output([str(go_bin / ("go.exe" if system == "windows" else "go")), "version"], text=True)
if "go" + lock["go"] + " " not in version:
    raise SystemExit("Unexpected compiler: " + version)
print(version.strip())
if os.getenv("GITHUB_PATH"):
    with open(os.environ["GITHUB_PATH"], "a") as output:
        output.write(str(go_bin) + "\n")
if os.getenv("GITHUB_ENV"):
    with open(os.environ["GITHUB_ENV"], "a") as output:
        output.write("GOTOOLCHAIN=local\nGOROOT=" + str(folder / "go") + "\n")
