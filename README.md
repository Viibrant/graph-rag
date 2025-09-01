# Litgraph

Graph-augmented semantic search for academic literature

<p align="center">
  <img src="docs/screenshot.png" alt="Litgraph screenshot" width="800"/>
  <br/>
  <em>Frontend: semantic results + graph view (mock data)</em>
</p>

## Features

- 📄 Fetch papers from ArXiv API
- 🧠 Queue papers for embedding (deferred, async)
- 🧮 Track paper ingestion state in SQLite index
- 📦 Index embeddings into Qdrant
- 🔍 Search Qdrant with fastembed support
- 🧩 Merge vector + (planned) graph hits
- ✅ Type-safe, testable, modular pipeline
- ⚙️ Health checks, typed interfaces, and task runner setup

## Usage

### Requirements

- Python 3.12+
- Node.js 20+
- Docker + Docker Compose

### Local dev (CPU by default)

```bash
make up-full        # Run full stack with CPU
make up-full USE_GPU=1  # Run with GPU (requires NVIDIA runtime)
```

Services:

- **API** → [http://localhost:8000/docs](http://localhost:8000/docs)
- **Qdrant UI** → [http://localhost:6333/dashboard](http://localhost:6333/dashboard)
- **Redis** → localhost:6379 (use `redis-cli`)

### Direct tasks (no Docker)

```bash
poe server     # Run the FastAPI backend
poe pipeline   # Run the end-to-end pipeline (logs steps)
poe test       # Run the tests
```

## Diagram

<details>
<summary>System architecture diagram</summary>

```mermaid
flowchart TD
    subgraph API
        A1[GET /search] --> P["run_pipeline()"]
    end

    subgraph Pipeline
        P --> F[Discover papers from ArXiv]
        F --> I[Update PaperIndex]
        I --> Q[Enqueue papers if not embedded]
        Q --> S[Semantic Search]
        S --> G[Get related from GraphStore]
        G --> M[Merge vector + graph results]
        M --> R[Return SearchResults]
    end

    subgraph Vector Store
        V1["Qdrant (hosted/local)"]
    end

    subgraph Embedding Worker
        W1["Reads Redis queue"]
        W1 --> E[Embed papers]
        E --> V[Upsert to Qdrant]
        V --> U[Update PaperIndex status]
    end

    subgraph Graph Store
        G1["(Planned) Neo4j / in-memory graph"]
    end

    S -->|vector hits| V1
    G -->|edges| G1
    G1 -->|related| G
```

</details>

Stack highlights:

- Backend: FastAPI + Pydantic + Poetry (with `poethepoet` task runner)
- Queue: Redis (Upstash or local)
- Vector DB: Qdrant
- Frontend: React + Vite + Tailwind
- Infra: Docker Compose + Fly.io

## Acknowledgements

Thank you to arXiv for use of its open access interoperability.

## License

MIT
