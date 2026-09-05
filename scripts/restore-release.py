"""Restore the reviewed compiled site from its integrity-checked transport parts."""
from pathlib import Path
import hashlib
import io
import tarfile

root = Path(__file__).resolve().parent.parent
payload = root / ".release-payload"
parts = sorted(payload.glob("site.tar.gz.part-*"))
assert parts, "Missing compiled release parts"
assert [p.name for p in parts] == [f"site.tar.gz.part-{i:03d}" for i in range(len(parts))], "Missing or misordered part"
data = b"".join(p.read_bytes() for p in parts)
assert hashlib.sha256(data).hexdigest() == (payload / "site.tar.gz.sha256").read_text().strip(), "Release archive checksum mismatch"
with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as archive:
    for member in archive.getmembers():
        path = Path(member.name)
        assert not path.is_absolute() and ".." not in path.parts and path.parts[0] == "site", "Unsafe archive path"
        assert member.isfile() or member.isdir(), "Unsupported archive entry"
    archive.extractall(root, filter="data")
print("Restored accepted compiled Web release.")

# Small game updates reuse the byte-identical engine in the base release.
overlay = payload / 'update.tar.gz'
if overlay.exists():
    update = overlay.read_bytes()
    expected = (payload / 'update.tar.gz.sha256').read_text().strip()
    assert hashlib.sha256(update).hexdigest() == expected, 'Release update checksum mismatch'
    with tarfile.open(fileobj=io.BytesIO(update), mode='r:gz') as archive:
        for member in archive.getmembers():
            path = Path(member.name)
            assert not path.is_absolute() and '..' not in path.parts and path.parts[0] == 'site', 'Unsafe update path'
            assert member.isfile(), 'Release updates contain regular files only'
        archive.extractall(root, filter='data')
    print('Applied integrity-checked compiled release update.')
