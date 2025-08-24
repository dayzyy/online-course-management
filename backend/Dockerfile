# Use the uv base image with Python and uv preinstalled
FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /usr/local/app

# Install tzdata for zoneinfo
RUN apk add --no-cache tzdata

COPY pyproject.toml uv.lock ./

RUN uv sync

COPY ./ ./

EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
