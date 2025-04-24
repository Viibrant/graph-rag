# graph-rag

A modular AI pipeline that fetches research papers from ArXiv, tracks their ingestion state, and queues them for embedding and indexing into Qdrant. Designed for scalable semantic + graph-augmented search (Graph-RAG).


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
        V1["Qdrant (hosted)"]
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

```bash
poe server     # Run the FastAPI backend
poe pipeline   # Run the end-to-end pipeline (logs steps)
poe test       # Run the tests
```

## TODO

- [x] Fetch papers from ArXiv API  
- [x] Parse + normalize metadata (title, abstract, authors, etc.)  
- [x] Implement `PaperIndex` to track ingestion state  
- [x] Add Redis-backed embedding queue  
- [x] Add `enqueue_missing()` to dedupe and defer processing  
- [x] Write unit tests for queuing logic  
- [x] Add semantic search using Qdrant fastembed  
- [x] Modularise pipeline into discovery, semantic, queue  
- [x] Add structured, typed `IngestEvent` system  
- [x] Return semantic search results via `/search`  
- [x] Deploy Qdrant to Fly.io  
- [x] Support `poe` task runner for DX  
- [ ] Implement embedding worker to consume queue and upsert to Qdrant  
- [ ] Track paper status post-embedding in `PaperIndex`  
- [ ] Implement `GraphStore` backend (e.g., NetworkX or Neo4j)  
- [ ] Define and compute paper "relatedness" (authors, topics, citations, etc.)  
- [ ] Add logic to update graph with related nodes  
- [ ] Fuse graph + vector results in `core.search()`  
- [ ] Handle papers with missing metadata gracefully  
- [ ] Add ranking logic to `SearchResult`  
- [ ] Build CLI or frontend for querying + graph viz  
- [ ] Populate Qdrant on startup (bootstrap/init script)  
- [ ] Deploy backend to Fly.io or similar  
- [ ] Snapshot Qdrant or add B2 backup support  
- [ ] Add metrics, health checks, and logging to pipeline  
