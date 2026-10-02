# first stage
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:0.12.22 /uv /bin/uv

# compile bytecode up front, copy instead of hardlinking from the cache mount,
# and use the image's Python rather than downloading one
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

WORKDIR /code
COPY pyproject.toml uv.lock ./

# install only the locked runtime dependencies into /code/.venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-install-project

# second unnamed stage
FROM python:3.14-slim

# Create a non-root user
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --gid 1001 app

WORKDIR /code

# copy only the virtual environment from the 1st stage image
COPY --from=builder --chown=app:app /code/.venv /code/.venv
COPY --chown=app:app tinaja_bot/ ./tinaja_bot/

USER app

ENV PATH="/code/.venv/bin:$PATH"

ENTRYPOINT [ "python", "-m", "tinaja_bot" ]
