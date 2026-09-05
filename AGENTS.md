# Release-mirror operating contract

This repository has one purpose: serve the latest accepted compiled Web release of *The Keepers* from GitHub Pages.

## Boundaries

- Work directly on `main`; do not introduce pull-request-only development flows.
- Do not add gameplay source, the living GDD, archive, roadmap, internal task data, or unreleased work.
- Accept compiled payloads only from an explicitly accepted tagged release of the private development repository.
- Never hand-edit `.wasm`, `.pck`, exported `.js`, worklets, or generated images.
- A minimal `index.html` disclosure layer may link controls and notices; keep it independent of gameplay.
- Preserve the Apache-2.0 `LICENSE` and `NOTICE` plus all Godot and third-party notices in every distribution.
- Mark modified redistributed files prominently as required by Apache-2.0.
- Do not use Git LFS for deployed files: GitHub Pages must receive the real payload, not pointer files.

## Required update sequence

1. Confirm the source release is accepted and all of its release workflow jobs pass.
2. Restore `site/` with `python3 scripts/restore-release.py`, then replace the nine generated Web-export files from the accepted release artifact.
3. Update version references and immutable provenance in `README.md`, `RELEASE.md`, and `site/about.html`.
4. Confirm `LICENSE`, `NOTICE`, and the exact Godot notice inventory accompany the compiled release.
5. Refresh `CHECKSUMS.sha256` with `scripts/update-checksums.sh`.
6. For a small update with the same engine, run `python3 scripts/pack-release-delta.py`; it stores changed compiled files and notices against the existing base parts. For a replacement engine or removed files, use `python3 scripts/pack-release.py`. Verify restoration plus `scripts/check.sh` before every release commit. Only reviewed compiled files and notices may enter these archives. Do not commit the generated `site/` directory.
7. Commit small, auditable release-mirror changes directly to `main`; wait for the Pages workflow to finish before calling a version live.

## Definition of released

A version is browser-released only when the `Publish playable Web release` workflow is green and the production URL returns the expected HTML, JavaScript, PCK, and WASM payloads. A committed artifact without a successful Pages deployment is staged, not released.
