# Release provenance

| Field | Accepted value |
|---|---|
| Product | The Keepers: Influence Arena 3D |
| Version | `v0.1.0-demo.4` |
| Channel | Prerelease demo |
| Accepted | 2026-09-05 |
| Source commit | `de2c9e2ffb0fec8318ea965cfc5ac0e42da6ad59` |
| Godot | `4.7.2` |
| Accepted release ZIP SHA-256 | `20c1661c230308899e2f09f454d7802a9ab7168b4fa6cd97d55dfd36ad612cfb` |
| License | Apache-2.0 for The Keepers portions; bundled notices retain their stated licenses |

All eight executable/image files match the accepted Web release exactly. The ninth export, `index.html`, retains its exact engine configuration and adds only the marked release-information disclosure. `site/about.html` lists the 3D camera controls and licenses.

The 39,514,754-byte Godot WebAssembly engine, loader, worklets and icons are byte-identical to the prior release. The existing base archive is retained; `.release-payload/update.tar.gz` replaces only changed compiled files and disclosure pages. Both archive layers have SHA-256 checks, and `CHECKSUMS.sha256` verifies every final deployed file.

No gameplay source, design archive or private project documents are included.
