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
│   └── distros.yml        # CI: syntax → build → test
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

## Validation

### Engine Validation

Before committing changes to `settings.yml`, validate that all engines in `enabled_engines` and `disabled_engines` are real SearXNG engines:

```bash
python3 -c "
import json
import urllib.request
from pathlib import Path

url = 'https://api.github.com/repos/searxng/searxng/contents/searx/engines'
req = urllib.request.Request(url, headers={'User-Agent': 'Python'})
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read())
    real_engines = sorted([item['name'].replace('.py', '') for item in data])

for settings_file in Path('distros').glob('*/settings.yml'):
    with open(settings_file) as f:
        content = f.read()
    in_section = None
    section = []
    for line in content.split('\n'):
        if line.strip() == 'enabled_engines:':
            in_section = 'enabled'
            section = []
        elif line.strip() == 'disabled_engines:':
            in_section = 'disabled'
            section = []
        elif in_section and line.startswith('  - '):
            engine = line.strip().replace('- ', '').strip()
            section.append(engine)
        elif in_section and not line.startswith('  - ') and not line.startswith('  #'):
            if in_section == 'enabled':
                invalid = [e for e in section if e not in real_engines]
                if invalid:
                    print(f'❌ {settings_file}: Invalid enabled engines: {invalid}')
                else:
                    print(f'✅ {settings_file}: All enabled engines valid')
            elif in_section == 'disabled':
                invalid = [e for e in section if e not in real_engines]
                if invalid:
                    print(f'❌ {settings_file}: Invalid disabled engines: {invalid}')
                else:
                    print(f'✅ {settings_file}: All disabled engines valid')
            in_section = None
"
```

Or use a simpler one-liner to check for common invalid engines:

```bash
grep -E '^\s+- (shopping|images|videos|music|news|files|ito|reddit|youtube|twitter|instagram|tiktok)\b' distros/*/settings.yml
```

This will show any lines using category names instead of actual engine names.

### CI/CD Validation

The `distros` workflow validates:
- Containerfile syntax (buildah bud)
- OCI archive build
- Container health check (HTTP 200 on /health endpoint)

## CI/CD

- **distros**: Runs on PR/push/manual. Three steps: syntax → build → test.
  - Use `workflow_dispatch` with `step` input to run specific step.
- **dependabot-sync**: Runs on PR (distro changes), daily, or manual. Ensures `dependabot.yml` stays in sync with `distros/`.
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
