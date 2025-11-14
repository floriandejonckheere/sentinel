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

### CLI Application (`cli/`)

The CLI is built with Python using the following stack:
- **Typer**: CLI framework for building the command-line interface
- **Pydantic**: Data validation and modeling
- **LangChain**: AI/LLM integration framework
- **Rich**: Terminal output formatting
- **httpx**: HTTP client for API requests
- **uv**: Fast Python package manager

### Web Application (`web/`)

Planned future development for a web-based interface and API to allow programmatic access to Sentinel's assessment capabilities.

### Core Components

- **Assessor**: Main class responsible for conducting assessments based on input parameters.
- **Assessment**: Data models defining the structure of assessment results.

## Development Workflow

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

1. **CISO-Ready Output**: All assessments should be presentation-ready for CISOs and security teams
2. **Source-Grounded**: All claims and data points should be traceable to authoritative sources
3. **Accuracy First**: Cutting-edge accuracy in risk assessment and recommendations
4. **Speed**: Deliver comprehensive assessments in minutes, not hours or days
5. **Defensible Decisions**: Provide enough context and evidence to defend tool adoption decisions

## Future Enhancements

- Web API for programmatic access
- Batch assessment capabilities
- Historical trend tracking
- Custom compliance framework support
- Integration with security tools (SIEM, vulnerability scanners)
- Report generation (PDF, HTML)
- Comparison mode (compare multiple tools side-by-side)

## License

Copyright (c) 2025 Trust UTU
