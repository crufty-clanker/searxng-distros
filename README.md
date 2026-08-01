# searxng-distros

Pre-configured SearXNG packages built as OCI containers using **buildah** / **podman**.

Each distro lives in its own subdirectory and is maintained/tested independently.

## Directory structure

```
.
├── distros/
│   ├── academia/         # Scholar, arXiv, PubMed, Crossref, OpenAlex
│   ├── archiver/         # Anna's Archive, Z-Library, Open Library
│   ├── devtools/         # Stack Exchange, GitHub, GitLab, PyPI, npm, crates
│   ├── news/             # Google News, Bing News, Reuters, Tagesschau
│   ├── osint/            # Google Images, Flickr, Unsplash, OpenStreetMap
│   └── purpleteam/       # NVD, GitHub Code, Hacker News, PrivacyWall
├── .github/
│   ├── workflows/
│   │   ├── distros.yml              # CI: syntax → build → test
│   │   ├── dependabot-sync.yml      # Sync dependabot.yml with distros/
│   │   └── engine-validation.yml    # Validate SearXNG engine names
│   ├── dependabot.yml         # Grouped dependency updates
│   └── actionlint.yaml        # actionlint suppressions
└── scripts/
    ├── regenerate-dependabot.sh  # Sync dependabot config with subdirs
    └── validate-engines.py       # Validate SearXNG engine names
```

## Available distros

| Distro | Focus |
|--------|-------|
| [`academia`](distros/academia/) | Google Scholar, arXiv, PubMed, Crossref, OpenAlex |
| [`archiver`](distros/archiver/) | Anna's Archive, Z-Library, Open Library |
| [`devtools`](distros/devtools/) | Stack Exchange, GitHub, GitLab, PyPI, npm, crates |
| [`news`](distros/news/) | Google News, Bing News, Reuters, Tagesschau |
| [`osint`](distros/osint/) | Google Images, Flickr, Unsplash, OpenStreetMap |
| [`purpleteam`](distros/purpleteam/) | NVD, GitHub Code, Hacker News, PrivacyWall |

## Adding a new distro

1. Create a subdirectory under `distros/` (e.g. `distros/my-distroname/`).
2. Add a `Containerfile` (or `.buildah` file).
3. Run `./scripts/regenerate-dependabot.sh` to update the dependabot config.
4. Commit everything — the CI will pick up the new distro automatically.

## CI workflows

| Workflow           | Trigger                          | What it does                                  |
|--------------------|----------------------------------|-----------------------------------------------|
| `distros`          | PR, push, or manual              | Three steps: syntax → build → test            |
| `dependabot-sync`  | PR (distro changes), daily, or manual | Checks `dependabot.yml` is in sync with `distros/`, opens PR if not |
| `engine-validation` | Manual or on PR                  | Validates all engines in settings.yml are real SearXNG engines |

## Engine Validation

Before committing changes to `settings.yml`, validate that all engines in `enabled_engines` and `disabled_engines` are real SearXNG engines using this Python script:

```bash
python3 << 'EOF'
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
                status = '❌' if invalid else '✅'
                print(f'{status} {settings_file}: {"Invalid: " + str(invalid) if invalid else "All valid"}')
            elif in_section == 'disabled':
                invalid = [e for e in section if e not in real_engines]
                status = '❌' if invalid else '✅'
                print(f'{status} {settings_file}: {"Invalid: " + str(invalid) if invalid else "All valid"}')
            in_section = None
EOF
```

## Building locally

```bash
# Syntax check
buildah bud --isolation chroot --quiet -f distros/my-distro/Containerfile distros/my-distro/

# Build OCI archive
buildah bud --format oci -f distros/my-distro/Containerfile -o /tmp/my-distro.tar distros/my-distro/

# Push to a registry
buildah push oci-archive:/tmp/my-distro.tar docker://registry.example.com/my-distro:1.0
```

## License

MIT — only the build scripts and CI config are in this repo.
