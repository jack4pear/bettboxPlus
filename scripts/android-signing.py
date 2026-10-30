"""Materialize this fork's persistent release key from GitHub Secrets."""
import base64
import os
from pathlib import Path

keys = ["BETTBOXPLUS_KEYSTORE_BASE64", "BETTBOXPLUS_STORE_PASSWORD", "BETTBOXPLUS_KEY_ALIAS", "BETTBOXPLUS_KEY_PASSWORD"]
missing = [key for key in keys if not os.getenv(key)]
if missing:
    raise SystemExit("Release blocked: missing persistent BettboxPlus signing secrets: " + ", ".join(missing))
root = Path(__file__).resolve().parents[1]
(root / "android/app/keystore.jks").write_bytes(base64.b64decode(os.environ[keys[0]], validate=True))
# Java Properties escapes are required for arbitrary secret values.
def escape(value):
    return value.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "\\r").replace("=", "\\=").replace(":", "\\:").replace(" ", "\\ ")
with (root / "android/local.properties").open("a") as out:
    out.write("\nstorePassword=" + escape(os.environ[keys[1]]) + "\n")
    out.write("keyAlias=" + escape(os.environ[keys[2]]) + "\n")
    out.write("keyPassword=" + escape(os.environ[keys[3]]) + "\n")
