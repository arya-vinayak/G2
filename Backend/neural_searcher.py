from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer
from qdrant_client.models import Filter

class NeuralSearcher:
    def __init__(self, collection_name: str):
        # Initialize the NeuralSearcher with the collection name
        self.collection_name = collection_name
        
        # Initialize the encoder model (SentenceTransformer) with a specific model
        # In this case, it's "all-MiniLM-L6-v2" and specify device as CUDA
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
        
        # Initialize Qdrant client with the provided URL
        self.qdrant_client = QdrantClient("http://localhost:6333")

    def search(self, text: str, filter: None):
        # Convert the input text into a vector representation using the pre-trained SentenceTransformer model
        vector = self.model.encode(text).tolist()

        if filter is None:
            # If no filter is provided, perform a simple vector similarity search
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                limit=1,  # Retrieve only the top 1 result
            )
        else:
            # If a filter is provided, construct a query filter based on the filter condition
            search_filter = Filter(**{
                "must": [{
                    "key": "name",  # Assuming the filter is applied to the 'name' field
                    "match": {
                        "value": filter  # Value to match in the 'name' field
                    }
                }]
            })
            
            # Perform a filtered search based on both the query vector and the provided filter
            search_result = self.qdrant_client.search(
                collection_name=self.collection_name,
                query_vector=vector,
                query_filter=search_filter,
                limit=1,  # Retrieve only the top 1 result
            )

        # Extract and return the payloads (stored data) from the search results
        payloads = [hit.payload for hit in search_result]
        return payloads
