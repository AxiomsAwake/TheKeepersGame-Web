"""Package an already reviewed and validated compiled site for Git transport."""
from pathlib import Path
import hashlib
import io
import subprocess
import tarfile

root = Path(__file__).resolve().parent.parent
subprocess.run(["bash", str(root / "scripts/check.sh")], check=True)
buffer = io.BytesIO()
with tarfile.open(fileobj=buffer, mode="w:gz", compresslevel=9) as archive:
    archive.add(root / "site", arcname="site")
data = buffer.getvalue()
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
    for member in archive.getmembers():
        if member.isfile():
            assert archive.extractfile(member).read() == (root / member.name).read_bytes()
payload = root / ".release-payload"
payload.mkdir(exist_ok=True)
# A full repack incorporates every change, so any older update is obsolete.
for stale in ['update.tar.gz', 'update.tar.gz.sha256']:
    (payload / stale).unlink(missing_ok=True)
for part in payload.glob("site.tar.gz.part-*"):
    part.unlink()
for number, offset in enumerate(range(0, len(data), 384000)):
    (payload / f"site.tar.gz.part-{number:03d}").write_bytes(data[offset:offset + 384000])
(payload / "site.tar.gz.sha256").write_text(hashlib.sha256(data).hexdigest() + "\n")
print(f"Packaged {len(data)} bytes of compiled release data.")
