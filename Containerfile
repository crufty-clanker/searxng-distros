# syntax=buildkit/dockerfile:1

# Base image: official SearXNG image
FROM searxng/searxng:latest

ARG distro

# --- Configuration (replace <distro> with your distro name) ---
COPY distros/${distro}/settings.yml /etc/searxng/settings.yml
COPY distros/${distro}/limiter.toml /etc/searxng/limiter.toml

# --- Themes (copies themes/<distro>/ into the image) ---
COPY themes/ /usr/searxng/searx/static/themes/

# --- Metadata ---
LABEL org.opencontainers.image.source="https://github.com/crufty-clanker/searxng-distros"
LABEL org.opencontainers.image.title="SearXNG for ${distro}"
LABEL org.opencontainers.image.description="SearXNG pre-configured for ${distro}"
