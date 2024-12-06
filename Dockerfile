FROM python:3.10

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.4.15 /uv /bin/uv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Compile bytecode
ENV UV_COMPILE_BYTECODE=1

# uv Cache
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

ENV PYTHONPATH=/app

# Copy scripts and ensure execute permissions for prestart.sh
COPY ./scripts /app/scripts
RUN chmod +x /app/scripts/prestart.sh

# Copy configuration and application files
COPY ./pyproject.toml ./uv.lock ./alembic.ini /app/
COPY ./app /app/app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Run prestart.sh before starting the app
CMD ["/bin/bash", "-c", "/app/scripts/prestart.sh && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4"]