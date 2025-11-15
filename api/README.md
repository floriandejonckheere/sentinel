# Sentinel API

## Get Project ID

```
export PROJECT_ID=$(gcloud config get-value project)
```

## Build

```
docker build --platform linux/amd64 -t gcr.io/${PROJECT_ID}/sentinel . && docker push gcr.io/${PROJECT_ID}/sentinel
```

## Deploy

```
gcloud run deploy sentinel  --image gcr.io/${PROJECT_ID}/sentinel  --region europe-north1  --platform managed  --allow-unauthenticated --set-env-vars GEMINI_API_KEY=${GEMINI_API_KEY}
```
