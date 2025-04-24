import xml.etree.ElementTree as ET
from typing import Any

import requests
from loguru import logger

from src.models import Paper

NAMESPACE = {"atom": "http://www.w3.org/2005/Atom"}


def get_text(node: ET.Element | None, required: bool = False) -> str:
    """
    Extracts text from an XML node, returning an empty string if the node is None or its text is None.

    Args:
        node (ET.Element | None): The XML node to extract text from.
        required (bool): If True, raises a ValueError if the node is required but not present.

    Returns:
        str: The text content of the node, stripped of leading and trailing whitespace.

    Raises:
        ValueError: If the node is required but not present.
    """
    if node is None or node.text is None:
        if required:
            raise ValueError("Missing required XML text field")
        logger.warning("Missing XML text field")
        return ""
    return node.text.strip()


def fetch_papers(query: str, max_results: int = 5) -> list[Paper]:
    api_url = "http://export.arxiv.org/api/query"
    params: dict[str, Any] = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
    }

    # Get data from arXiv API
    response = requests.get(api_url, params=params, timeout=10)
    response.raise_for_status()
    logger.debug(f"Response status code: {response.status_code}")

    # Parse the XML response
    root = ET.fromstring(response.content)
    papers: list[Paper] = []

    # Construct Paper objects per XML entry
    for entry in root.findall("atom:entry", NAMESPACE):
        # Extract paper details
        url: str = get_text(entry.find("atom:id", NAMESPACE), required=True)
        paper_id: str = url.partition("/abs/")[-1]
        title: str = get_text(entry.find("atom:title", NAMESPACE), required=True)
        abstract: str = get_text(entry.find("atom:summary", NAMESPACE), required=True)
        authors: list[str] = [
            get_text(author.find("atom:name", NAMESPACE), required=True)
            for author in entry.findall("atom:author", NAMESPACE)
        ]

        logger.debug(f"Paper ID: {url}")
        papers.append(Paper(id=paper_id, url=url, title=title, abstract=abstract, authors=authors))

    return papers
