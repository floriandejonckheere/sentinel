# Sentinel Project Overview

## Purpose

Sentinel is an AI-powered security assessor that transforms business decisions about IT tool adoption into comprehensive, source-grounded trust briefs. The system analyzes security risks, CVE trends, compliance signals, and provides risk scoring along with safer alternatives. Sentinel delivers CISO-ready and defendable decisions in minutes with cutting-edge accuracy.

## Project Structure

```
sentinel/
├── cli/                    # Command-line interface application
│   ├── cli.py             # Main CLI entry point
│   ├── assessor.py        # Core assessment logic
│   ├── assessment.py      # Pydantic data models
│   ├── pyproject.toml     # Python dependencies (uv-managed)
│   └── .venv/             # Virtual environment
├── web/                   # Web API and interface
├── README.md              # Project description
└── CLAUDE.md              # Project overview and documentation
```

## Architecture

### Command-line Interface (CLI)

Command-line utility that accepts either a tool name or URL as input, performs security assessments, and outputs detailed trust briefs.

### Web API and interface

To be developed in future iterations.

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

### Adding Dependencies

```bash
cd cli
uv add package-name
```

## Code style

## Workflow