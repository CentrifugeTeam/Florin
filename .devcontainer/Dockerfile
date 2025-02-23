FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

# The installer requires curl (and certificates) to download the release archive
COPY --from=ghcr.io/astral-sh/uv:0.4.9 /uv /bin/uv