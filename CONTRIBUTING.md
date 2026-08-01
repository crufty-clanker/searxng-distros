# Contributing to SearXNG Distros

Thank you for your interest in contributing! This guide will help you get started.

## Prerequisites

- [buildah](https://buildah.io/) (preferred) or [podman](https://podman.io/)
- Git

## Adding a New Distro

1. **Create the distro directory**
   ```bash
   mkdir -p distros/my-distroname
   ```

2. **Create a Containerfile**
   Start with a template like `distros/devtools/Containerfile`. Key requirements:
   - Use `# syntax=buildkit/dockerfile:1` as the first line
   - Include a multi-stage build (builder + runtime)
   - Create a non-root user (`searxng`)
   - Add OCI labels

3. **Add configuration files**
   - `settings.yml` — SearXNG engine configuration
   - `limiter.toml` — Rate limiting settings
   - `README.md` — Distro documentation

4. **Run the dependabot sync script**
   ```bash
   ./scripts/regenerate-dependabot.sh
   ```

5. **Test locally**
   ```bash
   # Syntax check
   buildah bud --isolation chroot --quiet -f distros/my-distroname/Containerfile distros/my-distroname/

   # Build OCI archive
   buildah bud --format oci -f distros/my-distroname/Containerfile -o /tmp/my-distroname.tar distros/my-distroname/
   ```

6. **Commit and push**
   ```bash
   git add distros/my-distroname/
   git add .github/dependabot.yml
   git commit -m "feat: add my-distroname distro"
   git push
   ```

## Running the CI Locally

The CI runs three steps: **syntax**, **build**, **test**.

To run all steps manually:
```bash
buildah bud --isolation chroot --quiet -f distros/my-distroname/Containerfile distros/my-distroname/
buildah bud --format oci -f distros/my-distroname/Containerfile -o /tmp/my-distroname.tar distros/my-distroname/

# Test (requires network)
CONTAINER=$(buildah from "oci-archive:/tmp/my-distroname.tar")
buildah run --isolation chroot "$CONTAINER" sh -c "python -m searx.webapp &"
sleep 5
curl --fail http://localhost:8080/health
buildah rm "$CONTAINER"
```

## Code Style

- **YAML**: 2-space indentation, no tabs
- **TOML**: Follow [TOML v1.0](https://toml.io/en/v1.0.0) spec
- **Containerfile**: One instruction per line, group related RUN commands
- **Shell**: Use `set -euo pipefail`, quote variables

## Dependabot Sync

After adding a new distro, run:

```bash
./scripts/regenerate-dependabot.sh
```

The `dependabot-sync-check` workflow also runs automatically on PRs that modify distros and will open a PR if `dependabot.yml` is out of sync.

## Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat: add new distro`
- `fix: correct workflow condition`
- `docs: update README`
- `chore: regenerate dependabot config`

## Security

- Never commit secrets (API keys, passwords, tokens)
- Use `secret_key` and `sign_key` placeholders; generate at build time
- Run containers as non-root user

## Questions?

Open an issue or PR — we'll help you get it merged!
