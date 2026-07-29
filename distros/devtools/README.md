# Devtools Distro

SearXNG pre-configured for software developers.

## What's enabled

- **Code platforms**: Stack Overflow, GitHub, GitLab
- **Documentation**: docs engine (MDN, Python, Rust, etc.)
- **Package registries**: PyPI, npm, crates, Cargo
- **Search**: Google, DuckDuckGo, Bing, Wikipedia
- **Academic**: Google Scholar

## What's disabled

Shopping, images, videos, music, news, files, social media (Reddit, Twitter, Instagram, TikTok, YouTube).

## Configuration

- `settings.yml` — engine whitelist, UI defaults, server config
- `limiter.toml` — rate limits (generous for dev workflow)

## Building

```bash
buildah bud -f distros/devtools/Containerfile -t devtools distros/devtools/
```

## Running

```bash
buildah run <container-id> -- /opt/searxng/bin/python -m searx.webapp
```

## Customization

Edit `settings.yml` to add/remove engines. The `enabled_engines` list is authoritative — any engine not listed is disabled.
