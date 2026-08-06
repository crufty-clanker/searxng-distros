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
| `distros`          | PR, push, or manual              | Four steps: syntax → build → test → test-run  |
| `dependabot-sync`  | PR (distro changes), daily, or manual | Checks `dependabot.yml` is in sync with `distros/`, opens PR if not |
| `engine-validation` | Manual or on PR                  | Validates all engines in settings.yml are real SearXNG engines |

The `test-run` job is the most reliable validation — it actually starts SearXNG and checks the logs for errors.

## Engine Validation

Before committing changes to `settings.yml`, validate that all engines are real SearXNG engines:

```bash
python3 scripts/validate-engines.py
```

This script fetches the real engine list from SearXNG master and validates all engines in all distros.

### SearXNG Configuration Format

SearXNG uses `use_default_settings: true` which loads the default engine list. To configure engines:

```yaml
use_default_settings: true

engines:
  # Keep only these engines (all others disabled)
  keep_only:
    - google
    - duckduckgo
    - bing
    - wikipedia
```

Or to remove specific engines:

```yaml
use_default_settings: true

engines:
  remove:
    - shopping
    - images
```

The `enabled_engines` and `disabled_engines` keys are **not standard SearXNG** and won't work.

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

This project is licensed under the GNU Affero General Public License (AGPL-3.0). See [LICENSE](./LICENSE) for more details.
