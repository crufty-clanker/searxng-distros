# searxng-distros

Pre-configured SearXNG packages built as OCI containers using **buildah** / **podman**.

Each distro lives in its own subdirectory and is maintained/tested independently.

## Directory structure

```
.
├── distros/              # Each distro gets its own subdir
│   ├── minimal/          # e.g. core SeX with no extras
│   ├── full/             # SeX + all built-in engines
│   └── ...
├── .github/
│   ├── workflows/
│   │   ├── syntax-check.yml   # Validates Dockerfiles on PR/push
│   │   └── build.yml          # Builds OCI images on tags
│   └── dependabot.yml         # Grouped dependency updates
└── scripts/
    └── regenerate-dependabot.sh  # Sync dependabot config with subdirs
```

## Adding a new distro

1. Create a subdirectory under `distros/` (e.g. `distros/my-distroname/`).
2. Add a `Dockerfile` (or `.dockerfile` / `.buildah` file).
3. Run `./scripts/regenerate-dependabot.sh` to update the dependabot config.
4. Commit everything — the CI will pick up the new distro automatically.

## CI workflows

| Workflow      | Trigger                          | What it does                                  |
|---------------|----------------------------------|-----------------------------------------------|
| `syntax-check`| PR or push (when Dockerfiles change) | Validates every `Dockerfile` with `buildah bud` |
| `build`       | Tag push (`v*`) or manual        | Builds OCI archives per distro, optionally pushes to registry |

## Building locally

```bash
# Syntax check
buildah bud --isolation chroot --quiet -f distros/my-distro/Dockerfile distros/my-distro/

# Build OCI archive
buildah bud --format oci -f distros/my-distro/Dockerfile -o /tmp/my-distro.tar distros/my-distro/

# Push to a registry
buildah push oci-archive:/tmp/my-distro.tar docker://registry.example.com/my-distro:1.0
```

## License

MIT — only the build scripts and CI config are in this repo.
