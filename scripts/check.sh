#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

required=(
  site/index.html
  site/index.js
  site/index.wasm
  site/index.pck
  site/index.png
  site/index.icon.png
  site/index.apple-touch-icon.png
  site/index.audio.worklet.js
  site/index.audio.position.worklet.js
  site/about.html
  site/legal/Apache-2.0.txt
  site/legal/NOTICE.txt
  site/legal/GODOT_COPYRIGHT.txt
  site/.nojekyll
)

for path in "${required[@]}"; do
  test -f "${path}"
done

test -z "$(find site -type l -print -quit)"
test ! -e site/source
sha256sum --check CHECKSUMS.sha256
python3 - <<'PY'
import json
from pathlib import Path
import re
site = Path('site')
config = json.loads(re.search(r'const GODOT_CONFIG = (.*);', (site / 'index.html').read_text())[1])
for name, size in config['fileSizes'].items():
    assert (site / name).stat().st_size == size, f'Truncated export: {name}'
assert (site / 'index.wasm').read_bytes()[:8] == b'\x00asm\x01\x00\x00\x00', 'Invalid WebAssembly header'
actual = {str(p) for p in site.rglob('*') if p.is_file()}
listed = {line.split('  ', 1)[1] for line in Path('CHECKSUMS.sha256').read_text().splitlines()}
assert actual == listed, 'Unexpected or unlisted deployed files'
PY
grep -Fq 'index.js' site/index.html
grep -Fq 'about.html' site/index.html
grep -Fq 'index.wasm' site/index.html
grep -Fq 'Apache-2.0.txt' site/about.html
grep -Fq 'NOTICE.txt' site/about.html
grep -Fq 'GODOT_COPYRIGHT.txt' site/about.html

server_log="$(mktemp)"
python3 -m http.server 4173 --directory site >"${server_log}" 2>&1 &
server_pid=$!
cleanup() {
  kill "${server_pid}" 2>/dev/null || true
  wait "${server_pid}" 2>/dev/null || true
  rm -f "${server_log}"
}
trap cleanup EXIT

for attempt in {1..20}; do
  if curl --fail --silent http://127.0.0.1:4173/index.html >/dev/null; then
    break
  fi
  if [[ "${attempt}" -eq 20 ]]; then
    cat "${server_log}"
    exit 1
  fi
  sleep 0.1
done

curl --fail --silent --show-error http://127.0.0.1:4173/index.js >/dev/null
curl --fail --silent --show-error http://127.0.0.1:4173/index.pck >/dev/null
curl --fail --silent --show-error --range 0-1023 http://127.0.0.1:4173/index.wasm >/dev/null
curl --fail --silent --show-error http://127.0.0.1:4173/about.html >/dev/null

printf 'Release mirror checks passed.\n'
