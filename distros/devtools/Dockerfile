# syntax=docker/dockerfile:1

FROM debian:bookworm-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv git && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/searxng && \
    /opt/searxng/bin/pip install --no-cache-dir searxng

FROM debian:bookworm-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 python3-lxml python3-redis libxml2-dev libxslt1-dev && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/searxng /opt/searxng

COPY settings.yml /etc/searxng/settings.yml
COPY limiter.toml /etc/searxng/limiter.toml

EXPOSE 8080

CMD ["/opt/searxng/bin/python", "-m", "searx.webapp"]
