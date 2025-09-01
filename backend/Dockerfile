FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS base
WORKDIR /app

# Cache deps (but not project code)
COPY backend/pyproject.toml backend/uv.lock* ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

# Final stage for CPU dev
FROM base AS cpu
WORKDIR /app
# Copy your code (but in dev we’ll override with a volume mount)
COPY backend/ /app/
RUN uv sync --frozen

ENV PYTHONUNBUFFERED=1
CMD ["uv", "run", "poe", "server"]

# Optional GPU stage
FROM base AS gpu
WORKDIR /app
COPY backend/ /app/

# Install GPU deps (torch+cuda, etc.)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system torch --index-url https://download.pytorch.org/whl/cu121

RUN uv sync --frozen

ENV PYTHONUNBUFFERED=1
CMD ["uv", "run", "poe", "server"]