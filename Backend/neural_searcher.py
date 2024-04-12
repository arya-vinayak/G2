from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter


class NeuralSearcher:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        # Initialize encoder model
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        # initialize Qdrant client
        self.qdrant_client = QdrantClient("http://localhost:6333")

    def search(self, text: str, filter: None):
        vector = self.model.encode(text).tolist()

        if filter is None:
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=1,  # 5 the most closest results is enough
            )
        else:
            ## Convert text query into vector
            search_filter = Filter(**{
                "must": [{
                    "key": "name",
                    "match": {
                        "value": filter
                    }
                }]
            })
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter=search_filter,
                limit=1,  # 5 the most closest results is enough
            )

        # search_result contains found vector ids with similarity scores along with the stored payload
        # In this function you are interested in payload only
        payloads = [hit.payload for hit in search_result]
        return payloads

