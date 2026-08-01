# OSINT Distro

SearXNG pre-configured for open-source intelligence gathering.

## What's enabled

- **Search**: Google, DuckDuckGo, Bing
- **Reference**: Wikipedia, Wikidata
- **Images**: Google Images, Flickr, Unsplash, Pexels, DeviantArt, Pixiv
- **Video**: YouTube, Vimeo
- **Maps**: OpenStreetMap, Wikicommons
- **News**: Reuters, Tagesschau

## What's disabled

Shopping, videos (Bing/Google), music, social media (Reddit, Twitter, Instagram), developer platforms (GitHub, GitLab), academic (arXiv, PubMed, DOI).

## Configuration

- `settings.yml` — engine whitelist, UI defaults, server config
- `limiter.toml` — rate limits (higher for OSINT research)

## Building

```bash
buildah bud -f distros/osint/Containerfile -t osint distros/osint/
```

## Running

```bash
buildah run <container-id> -- /opt/searxng/bin/python -m searx.webapp
```

## Customization

Edit `settings.yml` to add/remove engines. The `enabled_engines` list is authoritative — any engine not listed is disabled.
