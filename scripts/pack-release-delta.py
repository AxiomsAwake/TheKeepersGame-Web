"""Package changed compiled files against the committed base; never re-upload its engine."""
from pathlib import Path
import gzip
import hashlib
import io
import subprocess
import tarfile

root = Path(__file__).resolve().parent.parent
subprocess.run(['bash', str(root / 'scripts/check.sh')], check=True)
payload = root / '.release-payload'
parts = sorted(payload.glob('site.tar.gz.part-*'))
assert [p.name for p in parts] == [f'site.tar.gz.part-{i:03d}' for i in range(len(parts))]
base = b''.join(p.read_bytes() for p in parts)
assert hashlib.sha256(base).hexdigest() == (payload / 'site.tar.gz.sha256').read_text().strip()
with tarfile.open(fileobj=io.BytesIO(base), mode='r:gz') as archive:
    previous = {m.name: archive.extractfile(m).read() for m in archive.getmembers() if m.isfile()}
current = {p.relative_to(root).as_posix(): p.read_bytes() for p in (root / 'site').rglob('*') if p.is_file()}
assert not previous.keys() - current.keys(), 'A release with removed files requires a full repack.'
changes = {name: data for name, data in current.items() if data != previous.get(name)}
buffer = io.BytesIO()
with tarfile.open(fileobj=buffer, mode='w') as archive:
    for name, data in sorted(changes.items()):
        member = tarfile.TarInfo(name)
        member.size = len(data)
        member.mode = 0o644
        archive.addfile(member, io.BytesIO(data))
packed = gzip.compress(buffer.getvalue(), compresslevel=9, mtime=0)
(payload / 'update.tar.gz').write_bytes(packed)
(payload / 'update.tar.gz.sha256').write_text(hashlib.sha256(packed).hexdigest() + '\n')
print(f'Packaged {len(changes)} changed files in {len(packed)} bytes: {", ".join(sorted(changes))}')
