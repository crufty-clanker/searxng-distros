# Academia Distro

SearXNG pre-configured for academic research.

## What's enabled

- **Scholar**: Google Scholar, academic search
- **Repositories**: arXiv, PubMed, DOI, Crossref, Unpaywall, OpenAlex
- **General**: Google, DuckDuckGo, Bing, Wikipedia

## What's disabled

Shopping, images, videos, music, news, files, social media (Reddit, Twitter, Instagram, TikTok, YouTube), developer platforms (Stack Overflow, GitHub, GitLab).

## Configuration

- `settings.yml` — engine whitelist, UI defaults, server config
- `limiter.toml` — rate limits (moderate for research workflows)

## Building

```bash
buildah bud -f distros/academia/Containerfile -t academia distros/academia/
```

## Running

```bash
buildah run <container-id> -- /opt/searxng/bin/python -m searx.webapp
```

## Customization

Edit `settings.yml` to add/remove engines. The `enabled_engines` list is authoritative — any engine not listed is disabled.
