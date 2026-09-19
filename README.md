# Sasha's personal macOS builds

Unofficial personal builds of Zed (SashaEdit) and Warp (SashaTerm). Not affiliated with Zed Industries or Warp.

Casks are created only after the first published, verified release. A scheduled/manual workflow reads the public fork releases and opens a PR with exact versions and SHA-256 hashes. It does not publish or merge automatically and needs no cross-repository token.

After a cask appears on `main`:

```sh
brew install --cask sasha00123/tap/sasha-edit
brew install --cask sasha00123/tap/sasha-term
brew upgrade --cask sasha-edit sasha-term
```

These apps have separate names, IDs and data directories. They do not update from upstream. Current releases are ad-hoc signed, without Apple Developer ID/notarization. If macOS blocks the first launch, use Privacy & Security → Open Anyway for a build you trust. We do not disable Gatekeeper, remove quarantine automatically, or delete app data on uninstall.

Release/build/source details live in each fork's `distribution/README.md`. Zed application code is primarily GPL-3.0-or-later with Apache-2.0 components. Warp application code is AGPL-3.0 with MIT WarpUI components. Casks retain links to the corresponding source releases.

To activate: merge the setup PR, allow Actions to create PRs in repository settings, then run **Refresh personal casks** after publishing a release. CI validates generated Ruby and checks the manifest before opening the PR. Bot-created PRs do not themselves trigger GitHub Actions; the refresh job performs generation checks before pushing.
