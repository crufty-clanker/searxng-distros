# AGENTS.md — Guidelines for AI Agents

This project uses **buildah** and **podman** exclusively for OCI container operations. Docker is not used.

## Build System

- **Build tool**: `buildah` (preferred) or `podman`
- **Containerfile format**: `Containerfile` (not `Dockerfile`) or `.buildah` extension
- **Output format**: OCI archive (`oci-archive:`)
- **Syntax directive**: `# syntax=buildkit/dockerfile:1`

## Workflow

1. **Always run syntax checks** before committing:
   ```bash
   buildah bud --isolation chroot --quiet -f <path>/Containerfile <path>
   ```

2. **Build and test** locally when making changes:
   ```bash
   buildah bud --format oci -f <path>/Containerfile -o /tmp/test.tar <path>
   ```

3. **Commit after changes** — never leave uncommitted work.

## Project Structure

```
distros/<name>/
├── Containerfile      # Required: OCI build definition
├── settings.yml       # SearXNG configuration
├── limiter.toml       # Rate limiting config
└── README.md          # Distro documentation

.github/
├── workflows/
│   ├── distros.yml              # CI: syntax → build → test
│   ├── dependabot-sync.yml      # Sync dependabot.yml with distros/
│   └── engine-validation.yml    # Validate SearXNG engine names
├── dependabot.yml         # Grouped dependency updates per distro
└── actionlint.yaml        # actionlint suppressions

scripts/
├── regenerate-dependabot.sh  # Sync dependabot config with distros
└── validate-engines.py       # Validate SearXNG engine names
```

## Constraints

- **No Docker**: Use `buildah` or `podman` only
- **No Docker Compose**: Each distro is built independently
- **No external registries**: OCI archives are built locally, pushed only when requested
- **OCI format**: All builds produce `oci-archive:` format, not Docker format
- **Isolation**: Use `--isolation chroot` in CI to avoid rootless issues

## Adding a New Distro

1. Create `distros/<name>/` directory
2. Add `Containerfile` (or `.buildah` file)
3. Add configuration files (`settings.yml`, `limiter.toml`, etc.)
4. Add `README.md` documenting the distro
5. Run `./scripts/regenerate-dependabot.sh` to update dependabot config
6. Commit everything

## Validation

### Engine Validation

Before committing changes to `settings.yml`, validate that all engines are real SearXNG engines:

```bash
python3 scripts/validate-engines.py
```

This script:
- Fetches the real engine list from SearXNG master branch
- Validates all engines in all distros
- Reports invalid engines with counts
- Exits with code 1 if any invalid engines found

### SearXNG Configuration Format

SearXNG uses `use_default_settings: true` which loads the default engine list and then merges/overrides with your settings.

**To keep only specific engines:**

```yaml
use_default_settings: true

engines:
  keep_only:
    - google
    - duckduckgo
    - bing
    - wikipedia
```

**To remove specific engines:**

```yaml
use_default_settings: true

engines:
  remove:
    - shopping
    - images
```

The `enabled_engines` and `disabled_engines` keys are **not standard SearXNG** and won't work. Always use `engines.keep_only` or `engines.remove`.

### CI/CD Validation

The `distros` workflow validates:
- Containerfile syntax (buildah bud)
- OCI archive build
- Container health check (HTTP 200 on /health endpoint)

The `engine-validation` workflow validates:
- All engines in `engines.keep_only` are real SearXNG engines
- Creates issues for invalid engines
- Comments on PRs if issues found

## CI/CD

- **distros**: Runs on PR/push/manual. Four steps: syntax → build → test → test-run.
  - Use `workflow_dispatch` with `step` input to run specific step.
  - `test-run` runs the container and checks logs for errors (most reliable validation)
- **dependabot-sync**: Runs on PR (distro changes), daily, or manual. Ensures `dependabot.yml` stays in sync with `distros/`.
- **engine-validation**: Runs on PR/push/manual. Validates all SearXNG engine names are real. Creates issues for invalid engines.
- **dependabot**: Groups updates per distro subdir + GitHub Actions.

## Linting

- **actionlint**: GitHub Actions YAML validation (configured in `.github/actionlint.yaml`)
- **yamllint**: YAML syntax validation
- **buildah bud**: Containerfile syntax validation

## Examples

### Build a specific distro
```bash
buildah bud --format oci -f distros/devtools/Containerfile -o /tmp/devtools.tar distros/devtools/
```

### Push to registry
```bash
buildah push oci-archive:/tmp/devtools.tar docker://registry.example.com/devtools:1.0
```

### Run syntax check
```bash
buildah bud --isolation chroot --quiet -f distros/devtools/Containerfile distros/devtools/
```
