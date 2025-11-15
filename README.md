# Sentinel

AI-powered security assessor that transforms a business decision to use a certain IT tool into a source-grounded trust brief with CVE trends, compliance signals, risk scoring, and safer alternatives. Sentinel delivers CISO-ready and -defendable decisions in minutes, with cutting edge accuracy.

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


## Building

```bash
docker buildx build --platform linux/amd64 -t ghcr.io/floriandejonckheere/sentinel .
docker push ghcr.io/floriandejonckheere/sentinel
docker context create cloud --docker host=ssh://cloud@cloud.dejonckhee.re
docker --context cloud compose -f docker-compose.prod.yml up -d app
```

## License

Copyright (c) 2025 Trust UTU
