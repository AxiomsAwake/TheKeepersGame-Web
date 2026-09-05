# The Keepers — playable Web release

This public repository serves **Influence Arena `v0.1.0-demo.2`**, the first accepted playable proof of *The Keepers*.

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

## Repository boundary

This is a deliberately narrow binary release mirror, not the active game-design or source repository.

| Path | Purpose |
|---|---|
| `.release-payload/` | Integrity-checked archive parts containing only the accepted compiled Web export and notices |
| `site/` | Restored static Web export deployed to GitHub Pages; generated locally and in CI |
| `scripts/restore-release.py` | Restore the compiled site without an engine install or source checkout |
| `scripts/check.sh` | Fast integrity, structure, and local HTTP checks |
| `.github/workflows/pages.yml` | Validation and GitHub Pages deployment |
| `RELEASE.md` | Immutable release provenance and artifact identity |

The gameplay source, historical archive, living design document, internal roadmap, and active development history are intentionally absent.

## Deployment contract

Every push to `main` restores the compiled site with `python3 scripts/restore-release.py` and must pass `scripts/check.sh`. A successful run uploads only `site/` and deploys it through the `github-pages` environment. There is no package install and no generated dependency tree.

The Keepers portions of this binary release are licensed under the [Apache License 2.0](LICENSE); attribution is preserved in [NOTICE](NOTICE). The exported runtime uses Godot Engine under its own license and bundled third-party terms; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
