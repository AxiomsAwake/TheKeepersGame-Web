# The Keepers — playable Web release

This public repository serves **Influence Arena `v0.1.0-demo.4`**, the 3D command battle with clearer relay inspection of *The Keepers*.

## [Play in your browser](https://rmkn85.github.io/TheKeepersGame-Web/)

Establish the command link, choose a doctrine, deploy autonomous units, capture the relays, and collapse the challenger control network.

| Input | Command |
|---|---|
| `Enter` | Establish the command link |
| `1`, `2`, `3` | Choose Expand, Hold, or Assault doctrine |
| `Q`, `W` | Deploy a Scout or Guardian |
| Left click | Place an eight-second rally objective |
| Hover | Inspect unit intent or relay influence |
| `Space` | Pause command time |
| `R` | Restart the arena |
| Mouse wheel / right drag | Zoom / orbit the 3D camera |
| Arrow keys / `Home` | Pan / reset the camera |
| `V` / `I` | Ground view / influence overlay |

Relay inspection separates ownership from influence pressure and shows the control needed to claim a relay. Press Space to pause, then hover: the inspection card stays clear of its target and the battlefield center.

## Repository boundary

This is a deliberately narrow binary release mirror, not the active game-design or source repository.

| Path | Purpose |
|---|---|
| `.release-payload/` | Integrity-checked base parts plus a small compiled-file update; the engine is reused byte-for-byte |
| `site/` | Restored static Web export deployed to GitHub Pages; generated locally and in CI |
| `scripts/restore-release.py` | Restore the compiled site without an engine install or source checkout |
| `scripts/check.sh` | Fast integrity, structure, and local HTTP checks |
| `.github/workflows/pages.yml` | Validation and GitHub Pages deployment |
| `RELEASE.md` | Immutable release provenance and artifact identity |

The gameplay source, historical archive, living design document, internal roadmap, and active development history are intentionally absent.

## Deployment contract

Every push to `main` restores the compiled site with `python3 scripts/restore-release.py` and must pass `scripts/check.sh`. A successful run uploads only `site/` and deploys it through the `github-pages` environment. The validation job installs pinned browser-test dependencies in the runner temporary directory and exercises the actual compiled game in Chromium WebGL2. Those dependencies are not deployed.

The Keepers portions of this binary release are licensed under the [Apache License 2.0](LICENSE); attribution is preserved in [NOTICE](NOTICE). The exported runtime uses Godot Engine under its own license and bundled third-party terms; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
