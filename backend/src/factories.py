# backend/src/factories.py
import random
import uuid

import factory
from faker import Faker

from src import models

fake = Faker()


# --- Leaf factories ---
class PaperNodeFactory(factory.Factory):
    class Meta:
        model = models.PaperNode

    id = factory.LazyFunction(lambda: str(uuid.uuid4()))
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6))
    authors = factory.LazyFunction(lambda: [fake.name() for _ in range(random.randint(1, 3))])
    score = None
    related_ids = factory.LazyFunction(
        lambda: [str(uuid.uuid4()) for _ in range(random.randint(0, 3))]
    )
    centrality = factory.LazyFunction(random.random)


class GraphEdgeFactory(factory.Factory):
    class Meta:
        model = models.GraphEdge

    source = factory.LazyFunction(lambda: str(uuid.uuid4()))
    target = factory.LazyFunction(lambda: str(uuid.uuid4()))
    weight = factory.LazyFunction(random.random)
    type = "coauthor"


# --- Composite factory ---
class SearchResponseFactory(factory.Factory):
    """
    Factory for SearchResponse with tunable counts.
    Usage:
        SearchResponseFactory(num_results=10, num_nodes=20)
    """

    class Meta:
        model = models.SearchResponse

    # Extra params, not part of the Pydantic model
    num_results: int = 5
    num_nodes: int = 10

    @factory.lazy_attribute
    def graph(self) -> models.GraphData:
        nodes = PaperNodeFactory.build_batch(self.num_nodes)
        node_ids = [n.id for n in nodes]

        edges: list[models.GraphEdge] = []
        seen: set[tuple[str, str]] = set()

        for _ in range(self.num_nodes * 2):
            src, tgt = random.sample(node_ids, 2)  # guarantees src != tgt
            key = tuple(sorted((src, tgt)))
            if key in seen:
                continue
            seen.add(key)
            edges.append(
                models.GraphEdge(
                    source=src,
                    target=tgt,
                    weight=random.random(),
                    type="coauthor",
                )
            )

        return models.GraphData(nodes=nodes, edges=edges)

    @factory.lazy_attribute
    def results(self) -> list[models.PaperNode]:
        # Pick a subset of the graph’s nodes to be the “search hits”
        chosen = random.sample(self.graph.nodes, k=min(self.num_results, len(self.graph.nodes)))
        # Attach scores to the chosen results
        for node in chosen:
            node.score = round(random.random(), 3)

        return chosen
