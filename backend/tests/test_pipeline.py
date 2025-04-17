from src.pipeline import run_pipeline


def test_pipeline_yields_steps():
    events = list(run_pipeline("transformers"))
    steps = [e.step for e in events if e.type == "step"]
    assert steps == [
        "fetching_arxiv",
        "embedding",
        "vector_index",
        "graph_index",
        "semantic_search",
        "graph_search",
    ]
    assert any(e.type == "result" for e in events)