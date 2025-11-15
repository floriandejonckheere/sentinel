# Multi-stage Dockerfile for Sentinel
# Stage 1: Build frontend
FROM node:24-slim AS web

WORKDIR /app/web

# Copy web package files
COPY web/package*.json ./

# Install dependencies
RUN npm ci

# Copy web source
COPY web/ ./

# Build frontend
RUN npm run build

# Stage 2: Build and run backend
FROM python:3.13-slim AS backend

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir uv

# Copy unified project metadata and source code before install
COPY pyproject.toml /app/
COPY uv.lock /app/

# Install dependencies
RUN uv pip install --system .

# Copy backend source code
COPY api/ /app/api/
COPY cli/ /app/cli/

# Copy built frontend
COPY --from=web /app/web/dist /app/api/static

ENV PYTHONPATH=/app
ENV PORT=8080

WORKDIR /app/api
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "4", "--timeout", "0", "main:app"]
