FROM ghcr.io/astral-sh/uv:python3.11-bookworm AS base

# 1. Configuration: Set the venv location OUTSIDE the workdir (/app)
# This prevents the volume mount in docker-compose (.:/app) from overwriting/hiding the venv.
ENV UV_PROJECT_ENVIRONMENT="/venv"
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies into the specific environment location (/venv)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=/app/uv.lock \
    --mount=type=bind,source=pyproject.toml,target=/app/pyproject.toml \
    uv sync --frozen --no-dev

# ---------- Stage 2: Runtime ----------
FROM python:3.11-slim AS final

ENV PYTHONUNBUFFERED=1
# 2. Add the custom venv location to the PATH
ENV PATH="/venv/bin:$PATH"

WORKDIR /app

# 3. Copy the virtual environment from the base image to the isolated path
COPY --from=base /venv /venv

# Copy application source code
# (Note: In dev with docker-compose volumes, this is shadowed, but required for prod)
COPY app.py ./
COPY templates ./templates

EXPOSE 5001

CMD ["python", "app.py"]
