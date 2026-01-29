import os

import weaviate

from weaviate.config import AdditionalConfig, Timeout

# Only uses Weaviate Embeddings for now, so no additional headers are passed in
def get_weaviate_sync_client():
    return weaviate.connect_to_weaviate_cloud(
        cluster_url=os.environ.get("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
        additional_config=AdditionalConfig(
                timeout=Timeout(query=6000)
        ),    
    )

def get_weaviate_async_client():
    return weaviate.use_async_with_weaviate_cloud(
        cluster_url=os.environ.get("WEAVIATE_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY"))    
    )