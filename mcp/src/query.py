from weaviate.agents.query import QueryAgent

from src.utils import get_weaviate_sync_client

def ask(query: str) -> str:
    weaviate_sync_client = get_weaviate_sync_client()
    print(f"Querying Weaviate with query: {query}")
    '''
    collection = weaviate_sync_client.collections.get("IRPAPERS")
    response = collection.query.hybrid(
        query=query,
        limit=5,
    )
    print(response)
'''
    try:
        query_agent = QueryAgent(
            client=weaviate_sync_client,
            collections=["IRPAPERS"],
        )
        response = query_agent.ask(query)
        return response.final_answer
    finally:
        # Ensure we always close the connection, even if the request errors.
        weaviate_sync_client.close()