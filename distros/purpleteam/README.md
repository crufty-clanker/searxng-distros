# Purpleteam Distro

SearXNG pre-configured for security operations and threat intelligence.

## What's enabled

- **Search**: Google, DuckDuckGo, Bing
- **Reference**: Wikipedia, Wikidata
- **Security**: NVD (National Vulnerability Database), GitHub Code, Hacker News, PrivacyWall, SourceHut, Gitea
- **News**: Reuters, Tagesschau

## What's disabled

Shopping, images, videos, music, social media, developer platforms (GitHub search, GitLab), academic (arXiv, PubMed, DOI).

## Configuration

- `settings.yml` — engine whitelist, UI defaults, server config
- `limiter.toml` — rate limits (moderate for security research)

## Building

```bash
buildah bud -f distros/purpleteam/Containerfile -t purpleteam distros/purpleteam/
```

## Running

```bash
buildah run <container-id> -- /opt/searxng/bin/python -m searx.webapp
```

## Customization

Edit `settings.yml` to add/remove engines. The `enabled_engines` list is authoritative — any engine not listed is disabled.
