# Railway-optimized Dockerfile for Hermes Agent
# Runs the gateway service with dashboard on a single port
FROM ghcr.io/astral-sh/uv:0.11.6-python3.13-bookworm-slim AS uv_source
FROM node:22-bookworm-slim AS node_source

FROM debian:bookworm-slim

ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    ca-certificates curl python3 python-is-python3 ripgrep ffmpeg gcc \
    python3-dev libffi-dev procps git openssh-client && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -u 10000 -m -d /opt/data hermes

COPY --chmod=0755 --from=uv_source /usr/local/bin/uv /usr/local/bin/uvx /usr/local/bin/

COPY --chmod=0755 --from=node_source /usr/local/bin/node /usr/local/bin/
COPY --from=node_source /usr/local/lib/node_modules/npm /usr/local/lib/node_modules/npm
COPY --from=node_source /usr/local/lib/node_modules/corepack /usr/local/lib/node_modules/corepack
RUN ln -sf /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm && \
    ln -sf /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx && \
    ln -sf /usr/local/lib/node_modules/corepack/dist/corepack.js /usr/local/bin/corepack

WORKDIR /opt/hermes

# Copy hermes-agent source
COPY hermes-agent/package.json hermes-agent/package-lock.json ./
COPY hermes-agent/web/package.json web/
COPY hermes-agent/ui-tui/package.json ui-tui/
COPY hermes-agent/ui-tui/packages/hermes-ink/ ui-tui/packages/hermes-ink/

ENV npm_config_install_links=false
RUN npm install --prefer-offline --no-audit && \
    npm cache clean --force

# Python deps
COPY hermes-agent/pyproject.toml hermes-agent/uv.lock ./
RUN touch ./README.md
RUN uv sync --frozen --no-install-project --extra all --extra messaging --extra anthropic --extra bedrock --extra azure-identity

# Source code
COPY hermes-agent/ .

# Build web UI and TUI
RUN cd web && npm run build && \
    cd ../ui-tui && npm run build

# Permissions
USER root
RUN chmod -R a+rX /opt/hermes && \
    chown -R hermes:hermes /opt/hermes/.venv /opt/hermes/ui-tui /opt/hermes/node_modules

# Install hermes as editable
RUN uv pip install --no-cache-dir --no-deps -e "."

# Runtime env
ENV HERMES_WEB_DIST=/opt/hermes/hermes_cli/web_dist
ENV HERMES_TUI_DIR=/opt/hermes/ui-tui
ENV HERMES_HOME=/opt/data
ENV PATH="/opt/hermes/.venv/bin:/opt/data/.local/bin:${PATH}"

RUN mkdir -p /opt/data && chown hermes:hermes /opt/data

# Copy config and env into the data dir
COPY --chown=hermes:hermes config.yaml /opt/data/config.yaml

USER hermes

# Railway injects PORT env var — start script reads it
COPY --chmod=0755 railway-start.sh /opt/hermes/railway-start.sh
CMD ["/opt/hermes/railway-start.sh"]
