# syntax=docker/dockerfile-upstream:master-labs

FROM python:3.13-alpine AS build
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    : \
    && uv sync --no-dev --locked \
    && :

FROM python:3.13-alpine AS base
COPY --parents --from=build /app/.venv /
WORKDIR /app
COPY ./src ./
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=0

FROM base AS production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
