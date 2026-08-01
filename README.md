# searxng-distros

Pre-configured SearXNG packages built as OCI containers using **buildah** / **podman**.

Each distro lives in its own subdirectory and is maintained/tested independently.

## Directory structure

```
.
├── distros/
│   ├── devtools/         # SearXNG for software developers
│   │   ├── Containerfile
│   │   ├── settings.yml
│   │   ├── limiter.toml
│   │   └── README.md
│   └── ...               # Other distros (academia, news, osint, ...)
├── .github/
│   ├── workflows/
│   │   ├── distros.yml        # CI: syntax → build → test
│   │   └── release.yml        # Builds OCI archives on tags
│   ├── actions/
│   │   └── install-buildah/   # Composite action for buildah/podman
│   ├── dependabot.yml         # Grouped dependency updates
│   └── actionlint.yaml        # actionlint suppressions
└── scripts/
    └── regenerate-dependabot.sh  # Sync dependabot config with subdirs
```

## Available distros

| Distro | Focus |
|--------|-------|
| [`devtools`](distros/devtools/) | Stack Overflow, GitHub, docs, package registries |
| `academia` | Scholar, arXiv, PubMed, DOI |
| `news` | News sources, fact-checking, multilingual |
| `archiver` | Web archive, Wayback Machine |
| `purpleteam` | Security advisories, CVE, NVD |
| `osint` | Public data correlation, Shodan, Censys |

## Adding a new distro

1. Create a subdirectory under `distros/` (e.g. `distros/my-distroname/`).
2. Add a `Containerfile` (or `.buildah` file).
3. Run `./scripts/regenerate-dependabot.sh` to update the dependabot config.
4. Commit everything — the CI will pick up the new distro automatically.

## CI workflows

| Workflow  | Trigger                          | What it does                                  |
|-----------|----------------------------------|-----------------------------------------------|
| `distros` | PR, push, or manual              | Three steps: syntax → build → test            |

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
