import json
import threading
from typing import Annotated

from fastmcp import FastMCP, Context
from fastmcp.server.lifespan import lifespan

from src.utils import get_weaviate_sync_client
from src.startup import startup

_data_ready = False


def _background_startup():
    global _data_ready
    startup()
    _data_ready = True


@lifespan
async def weaviate_lifespan(server):
    """Initialize Weaviate client and ensure collection is ready."""
    client = get_weaviate_sync_client()
    thread = threading.Thread(target=_background_startup, daemon=True)
    thread.start()
    try:
        yield {"weaviate_client": client}
    finally:
        client.close()


mcp = FastMCP(
    name="IRPAPERS",
    instructions=(
        "This server provides access to a collection of academic papers "
        "on Information Retrieval and Large Language Models. "
        "Use the 'ask' tool to query the paper collection with natural language questions."
    ),
    lifespan=weaviate_lifespan,
)


@mcp.tool
def ask(
    query: Annotated[str, "A natural language question about IR papers"],
) -> str:
    """Ask a question about the IRPAPERS collection of academic papers on Information Retrieval and LLMs.

    The question is answered by a Weaviate QueryAgent that searches over
    page-level multimodal embeddings of 166 research papers (3,230 pages).
    """
    if not _data_ready:
        return "The IRPAPERS collection is still loading. Please try again in a few minutes."

    from weaviate.agents.query import QueryAgent

    client = get_weaviate_sync_client()
    try:
        query_agent = QueryAgent(
            client=client,
            collections=["IRPAPERS"],
        )
        response = query_agent.ask(query)
        return response.final_answer
    finally:
        client.close()

@mcp.resource("irpapers://status")
def get_status(ctx: Context) -> str:
    """Current status of the IRPAPERS collection."""
    client = ctx.lifespan_context["weaviate_client"]
    collection = client.collections.get("IRPAPERS")
    count = len(collection)
    return json.dumps({
        "collection": "IRPAPERS",
        "document_count": count,
    })


@mcp.resource("irpapers://info")
def get_info() -> str:
    """Information about the IRPAPERS collection and what it contains."""
    return json.dumps({
        "name": "IRPAPERS",
        "description": (
            "A multimodal collection of 166 academic papers on Information Retrieval "
            "and Large Language Models, indexed as 3,230 page-level documents with "
            "multi-vector embeddings (MUVERA encoding) in Weaviate."
        ),
        "total_papers": 166,
        "total_pages": 3230,
        "embedding_type": "MultiVector (multi2vec_weaviate with MUVERA encoding)",
        "properties": ["title", "page_number", "page_image"],
        "data_source": "weaviate/irpapers-docs (HuggingFace)",
    })


if __name__ == "__main__":
    mcp.run()
