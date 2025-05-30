# Qdrant on Fly.io

Deploys a persistent Qdrant instance using Fly.io.

## Setup

1. **Login & Init**

```bash
fly auth login
cd infra/qdrant-fly
fly launch --name qdrant-graph-rag --no-deploy
```

2. **Create Volume**

```bash
fly volumes create qdrant_data --size 1 --region lhr
```

3. **Deploy**

```bash
fly deploy
```

## Usage

- Qdrant runs at: `http://qdrant-graph-rag.fly.dev:80`
- Example client setup:

```python
QdrantClient(host="qdrant-graph-rag.fly.dev", port=80)
```

## Environment

Add to `.env` in project root:

```env
QDRANT_HOST=qdrant-graph-rag.fly.dev
QDRANT_PORT=80
```

## Files

- `Dockerfile` – base image
- `fly.toml` – config
