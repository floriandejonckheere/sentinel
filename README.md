# Sentinel

AI-powered security assessor that transforms a business decision to use a certain IT tool into a source-grounded trust brief with CVE trends, compliance signals, risk scoring, and safer alternatives. Sentinel delivers CISO-ready and -defendable decisions in minutes, with cutting edge accuracy.

This project was created as a submission to the [Reputation Recon: AI-Powered Software Trust Assessment](CHALLENGE.md) challenge by WithSecure at [Junction 2025](https://hackjunction.com/).

🚀 [Live Demo](https://sentinel.dejonckhee.re)

📹 [Watch Demo Video](https://github.com/floriandejonckheere/sentinel/raw/main/Sentinel.mp4)

<p align="center" width="100%">
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot001.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot001.png" width="49%" height="auto"></a>
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot002.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot002.png" width="49%" height="auto"></a>
</p>

<p align="center" width="100%">
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot003.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot003.png" width="49%" height="auto"></a>
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot004.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot004.png" width="49%" height="auto"></a>
</p>

<p align="center" width="100%">
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot005.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot005.png" width="49%" height="auto"></a>
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot006.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot006.png" width="49%" height="auto"></a>
</p>

<p align="center" width="100%">
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot007.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot007.png" width="49%" height="auto"></a>
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot008.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot008.png" width="49%" height="auto"></a>
</p>

<p align="center" width="100%">
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot009.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot009.png" width="49%" height="auto"></a>
    <a href="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot010.png"><img src="https://github.com/floriandejonckheere/sentinel/raw/main/screenshot010.png" width="49%" height="auto"></a>
</p>

## Installation

Please ensure you have Docker installed on your system.

## Usage

```bash
docker compose up -d
```

The application will be available at [http://localhost:5137](http://localhost:5137).
The frontend is served at `/app`, while the backend API is accessible at `/api`.

## Building

For your convenience, a Dockerfile is provided to build a production-ready image.
The image uses Gunicorn to serve the static files and FastAPI backend.

To build the image, run:

```bash
docker build -t ghcr.io/floriandejonckheere/sentinel .
```

To run the image, run:

```bash
docker run -p 8080:8080 ghcr.io/floriandejonckheere/sentinel
```

Or use the `docker-compose.prod.yml` file.

## License

Copyright (c) 2025 Trust UTU
