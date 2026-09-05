#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

find site -type f -print0 \
  | sort -z \
  | xargs -0 sha256sum \
  > CHECKSUMS.sha256

printf 'Updated CHECKSUMS.sha256.\n'

