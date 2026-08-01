# Archiver Distro

SearXNG pre-configured for web archiving and preservation.

## What's enabled

- **Search**: Google, DuckDuckGo, Bing
- **Reference**: Wikipedia, Wikidata
- **Archives**: Anna's Archive, Z-Library, Open Library, Internet Archive

## What's disabled

Shopping, images ( Bing/Google), videos, music, social media, developer platforms, news sources.

## Configuration

- `settings.yml` — engine whitelist, UI defaults, server config
- `limiter.toml` — rate limits (moderate for archival research)

## Building

```bash
buildah bud -f distros/archiver/Containerfile -t archiver distros/archiver/
```

## Running

```bash
buildah run <container-id> -- /opt/searxng/bin/python -m searx.webapp
```

## Customization

Edit `settings.yml` to add/remove engines. The `enabled_engines` list is authoritative — any engine not listed is disabled.
