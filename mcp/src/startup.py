import os
import time

from datasets import load_dataset
import weaviate
from weaviate.classes.config import Configure, Property, DataType

from src.utils import get_weaviate_sync_client
from src.config import IRPAPERS_DOCS_COUNT, LOUD_STARTUP

def startup():
    weaviate_sync_client = get_weaviate_sync_client()
    if not _check_if_collection_exists(weaviate_sync_client):
        _create_irpapers_weaviate_collection(weaviate_sync_client)
    if not _check_if_collection_has_data(weaviate_sync_client):
        _load_page_images_into_weaviate_collection(weaviate_sync_client)
    weaviate_sync_client.close()

def _check_if_collection_exists(weaviate_sync_client):
    if weaviate_sync_client.collections.exists("IRPAPERS"):
        return True
    else:
        return False

def _check_if_collection_has_data(weaviate_sync_client):
    if len(weaviate_sync_client.collections.get("IRPAPERS")) == IRPAPERS_DOCS_COUNT:
        return True
    else:
        return False

def _create_irpapers_weaviate_collection(weaviate_sync_client):
    weaviate_sync_client.collections.create(
            name="IRPAPERS",
            description="placeholder...",
            vector_config=Configure.MultiVectors.multi2vec_weaviate(
                name="document",
                image_field="page_image",
                encoding=Configure.VectorIndex.MultiVector.Encoding.muvera(),
                vector_index_config=Configure.VectorIndex.hnsw(
                    ef=256,
                )
            ),
            properties=[
                Property(name="title", data_type=DataType.TEXT),
                Property(name="page_number", data_type=DataType.INT),
                Property(name="page_image", data_type=DataType.BLOB),
            ]
        )

def _load_page_images_into_weaviate_collection(weaviate_sync_client):
    dataset = load_dataset("weaviate/irpapers-docs")["train"]
    dataset_dict = []
    for item in dataset:
        dataset_dict.append(dict(item))
    time_start = time.perf_counter()
    with weaviate_sync_client.batch.fixed_size(batch_size=20) as batch:
        for i, properties in enumerate(dataset_dict, start=1):
            props={
                "title": properties["pdf_title"],
                "page_number": int(properties["page_number"]),
                "page_image": properties["base64_str"],
            }
            batch.add_object(collection="IRPAPERS", properties=props)
            
            if LOUD_STARTUP and i % 100 == 0:
                elapsed = time.perf_counter() - time_start
                rate = i / max(elapsed, 1e-9)
                print(f"\033[92mInserted {i} objects ({elapsed:.1f}s, {rate:.1f} objs/s)\033[0m")

            total = i
            
        if LOUD_STARTUP:
            elapsed = time.perf_counter() - time_start
            rate = total / max(elapsed, 1e-9)
            print(f"\033[92mInserted {total} objects ({elapsed:.1f}s, {rate:.1f} objs/s)\033[0m")