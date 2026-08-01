# News Distro

SearXNG pre-configured for news and fact-checking.

## What's enabled

- **News**: Google News, Bing News, Finnish News, Ledectome
- **Search**: Google, DuckDuckGo, Bing
- **Reference**: Wikipedia, Wikidata

## What's disabled

Shopping, images, videos, music, files, social media (Reddit, Twitter, Instagram, TikTok, YouTube), developer platforms (Stack Overflow, GitHub, GitLab), academic (arXiv, PubMed, DOI).

## Configuration

- `settings.yml` — engine whitelist, UI defaults, server config
- `limiter.toml` — rate limits (higher for news consumption)

## Building

```bash
buildah bud -f distros/news/Containerfile -t news distros/news/
```

## Running

```bash
buildah run <container-id> -- /opt/searxng/bin/python -m searx.webapp
```

## Customization

Edit `settings.yml` to add/remove engines. The `enabled_engines` list is authoritative — any engine not listed is disabled.
