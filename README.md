# Project Setup & Commands

## Environment Variables
Create a `.env` file in the root directory by copying `.env.sample`:

```bash
cp .env.sample .env
```

Then fill in your actual credentials (like POSTGRES_USER, POSTGRES_PASSWORD, SECRET_KEY).

> **Note:** Inside Docker, the `POSTGRES_HOST` should be set to `db`, which is the name of the database service in `docker-compose.yml`.
This allows the backend container to connect to the database container.

# Setting up the tables

## Run migrations inside the backend container:
```bash
docker-compose run --rm backend uv run python makemigrations
docker-compose run --rm backend uv run python migrate
```

# Running the DB And API

```bash
docker-compose up --build
```

# Running tests
```bash
docker-compose run --rm backend uv run pytest
```

# Accessing API docs (Swagger)

## After running the API, docs can be viewed at `localhost:8000/api/v1/docs`
