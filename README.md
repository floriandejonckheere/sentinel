# Sentinel

AI-powered security assessor that transforms a business decision to use a certain IT tool into a source-grounded trust brief with CVE trends, compliance signals, risk scoring, and safer alternatives. Sentinel delivers CISO-ready and -defendable decisions in minutes, with cutting edge accuracy.

## Building

```bash
docker buildx build --platform linux/amd64 -t ghcr.io/floriandejonckheere/sentinel .
docker push ghcr.io/floriandejonckheere/sentinel
docker context create cloud --docker host=ssh://cloud@cloud.dejonckhee.re
docker --context cloud compose -f docker-compose.prod.yml up -d app
```

## License

Copyright (c) 2025 Trust UTU
