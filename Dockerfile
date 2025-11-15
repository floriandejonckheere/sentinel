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
FROM python:3.14-slim AS backend

WORKDIR /app

# Install build dependencies for compiling Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

# Install uv for Python package management
RUN pip install --no-cache-dir uv

# Copy CLI module first (since API depends on it)
COPY cli/pyproject.toml cli/uv.lock* /app/cli/

# Install CLI dependencies
WORKDIR /app/cli
RUN uv sync --frozen

# Copy API dependencies
COPY api/pyproject.toml api/uv.lock* /app/api/

# Install API dependencies
WORKDIR /app/api
RUN uv sync --frozen

# Copy CLI source code
COPY cli/ /app/cli/

# Copy API source code
COPY api/ /app/api/

# Copy built frontend from previous stage
COPY --from=web /app/web/dist /app/api/static

# Set Python path to include CLI directory
ENV PYTHONPATH=/app/cli:/app/api
ENV PORT=8080

# Run the application with uv
WORKDIR /app/api
CMD ["uv", "run", "gunicorn", "--bind", ":8080", "--workers", "2", "--threads", "4", "--timeout", "0", "main:app"]
