# Release provenance

| Field | Accepted value |
|---|---|
| Product | The Keepers: Influence Arena 3D |
| Version | `v0.1.0-demo.3` |
| Channel | Prerelease demo |
| Accepted | 2026-09-05 |
| Source commit | `2c7c67300c90ae24219cad9866a04ec23ec7b9a5` |
| Godot | `4.7.2` |
| Accepted release ZIP SHA-256 | `0b971d769a879c388d527e8c134aa4653463bc0894f3f4baf0ace8c1da8f0c3b` |
| License | Apache-2.0 for The Keepers portions; bundled notices retain their stated licenses |

All eight executable/image files match the accepted Web release exactly. The ninth export, `index.html`, retains its exact engine configuration and adds only the marked release-information disclosure. `site/about.html` lists the 3D camera controls and licenses.

The 39,514,754-byte Godot WebAssembly engine, loader, worklets and icons are byte-identical to the prior release. The existing base archive is retained; `.release-payload/update.tar.gz` replaces only changed compiled files and disclosure pages. Both archive layers have SHA-256 checks, and `CHECKSUMS.sha256` verifies every final deployed file.

No gameplay source, design archive or private project documents are included.
