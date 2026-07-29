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
│   ├── syntax-check.yml   # Auto-discovers Containerfiles, runs buildah syntax check
│   └── build.yml          # Builds OCI archives on tags
├── actions/install-buildah/   # Composite action for CI
├── dependabot.yml         # Grouped dependency updates per distro
└── actionlint.yaml        # actionlint suppressions

scripts/
└── regenerate-dependabot.sh  # Sync dependabot config with distros
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

## CI/CD

- **syntax-check**: Runs on PR/push when Containerfiles change. Auto-discovers subdirs.
- **build**: Runs on tag push (`v*`) or manual dispatch. Builds OCI archives per distro.
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
