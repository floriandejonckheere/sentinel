# Sentinel Project Overview

## Purpose

Sentinel is an AI-powered security assessor that transforms business decisions about IT tool adoption into comprehensive, source-grounded trust briefs. The system analyzes security risks, CVE trends, compliance signals, and provides risk scoring along with safer alternatives. Sentinel delivers CISO-ready and defendable decisions in minutes with cutting-edge accuracy.

## Project Structure

```
sentinel/
├── cli/                    # Command-line interface application
│   ├── cli.py             # Main CLI entry point
│   ├── assessor.py        # Core assessment logic
│   ├── assessment.py      # Assessment data model
│   ├── pyproject.toml     # Python dependencies (uv-managed)
│   └── .venv/             # Virtual environment
├── api/                    # Flask REST API
│   ├── sentinel/          # Flask application package
│   │   └── __init__.py    # App factory and routes
│   ├── main.py            # API entry point
│   ├── pyproject.toml     # Python dependencies (uv-managed)
│   └── Dockerfile         # Container configuration
├── web/                    # React + TypeScript web interface
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── App.tsx        # Main app component
│   │   ├── main.tsx       # Application entry point
│   │   └── index.css      # Global styles with Tailwind
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite configuration
│   └── tailwind.config.js # Tailwind configuration
├── docker-compose.yml      # Docker compose configuration
├── README.md              # Project description
└── CLAUDE.md              # Project overview and documentation
```

## Architecture

### Command-line Interface (CLI)

Command-line utility that accepts either a tool name or URL as input, performs security assessments, and outputs detailed trust briefs.
Located in `cli/`.

### Application Programming Interface (API)

Flask-based REST API for security assessments.
Located in `api/`.

**Running the API:**

```bash
# From the project root
cd api

# Install dependencies
uv sync

# Run locally
uv run python main.py

# Run with gunicorn (production)
uv run gunicorn --bind :8080 --workers 2 --threads 4 main:app
```

The API will be available at `http://localhost:8080`

**Endpoints:**
- `GET /health` - Health check
- `GET /assessments` - List all assessments
- `POST /assessments` - Create new assessment (accepts `name` or `url` parameter)

### Web Interface

React + TypeScript frontend with TailwindCSS for the assessment workflow.
Located in `web/`.

**Running the Web App:**

```bash
# From the project root
cd web

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

The web app will be available at `http://localhost:5173` (development)

### Running the CLI

```bash
# From the project root
cd cli

# Run with name
uv run python cli.py --name "My Application"

# Run with URL
uv run python cli.py --url "https://example.com"

# Get help
uv run python cli.py --help
```

### Running with Docker Compose

```bash
# From the project root
docker-compose up

# Build and run in detached mode
docker-compose up -d --build

# Stop services
docker-compose down
```

The API will be available at `http://localhost:8080`

### Adding Dependencies

**CLI:**
```bash
cd cli
uv add package-name
```

**API:**
```bash
cd api
uv add package-name
```

**Web:**
```bash
cd web
npm install package-name
```

## Code style

## Workflow