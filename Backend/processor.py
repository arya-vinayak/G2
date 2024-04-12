# Import necessary libraries
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from neural_searcher import NeuralSearcher  # Import your NeuralSearcher class
import redis  # Import the Redis library for connection
import json  # Import JSON library for handling JSON data

# Connect to Redis server
r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)
print("connected to redis")

# Create a pub/sub object to listen for incoming messages from a Redis channel
mobile = r.pubsub()
mobile.subscribe('newProductsSourceForge')

# Load pre-trained SentenceTransformer model for text encoding
model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
print("Model loaded successfully")

# Initialize NeuralSearcher for product search
neural_searcher = NeuralSearcher("G2products")
print("Neural Searcher loaded successfully")

# Function to calculate cosine similarity between two strings
def cosine_similarity_between_strings(string1, string2): 
    vector1 = model.encode(string1)  # Encode first string
    vector2 = model.encode(string2)  # Encode second string

    # Reshape the vectors for cosine similarity calculation
    vector1 = vector1.reshape(1, -1)
    vector2 = vector2.reshape(1, -1)

    # Calculate cosine similarity between the two vectors
    similarity_score = cosine_similarity(vector1, vector2)[0][0]

    return similarity_score

# Function to get similar products based on a product name
def get_similar_products(product_name, filter=None):
    similar_products = neural_searcher.search(product_name, filter)
    return similar_products

# Function to calculate similarity score between two products
def get_similarity_score(product1, product2):
    if(product1["name"] == product2["name"]):
        return 1.0
    if(product1["description"] == None):
        return 0.0

    similarity_score_names = cosine_similarity_between_strings(product1["name"], product2["name"])
    similarity_score_descriptions = cosine_similarity_between_strings(product1["description"], product2["description"])
## We have performed a weighted average of the similarity scores for the product names and descriptions.(60% for names and 40% for descriptions)
    similarity_score =  0.6 * similarity_score_names + 0.4 * similarity_score_descriptions

    return similarity_score

# Function to process incoming product
def process_product(product):
    similar_products = get_similar_products(product["name"])
    similarity_score = get_similarity_score(product, similar_products[0])
    if similarity_score > 0.85:
        print("Product already exists")
    else:
        print("Product not found")
        Products_Not_Exist.append(product)

# Function to save products not found to a JSON file
def save_products_not_found():
    try:
        with open("products_not_found.json", "r") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    for product in Products_Not_Exist:
        if product not in existing_data:
            existing_data.append(product)

    with open("products_not_found.json", "w") as f:
        json.dump(existing_data, f)

count = 0
Products_Not_Exist = []

# Listen for incoming messages from the Redis pub/sub channel
for message in mobile.listen():
    count += 1
    if message['type'] == 'message':
        try:
            print(f"Received message: {message['data']}")
            data = json.loads(message['data'])
            print(f"Decoded message: {data.get('description')}")
            process_product(data)
            print("number processed:")
            print(count)
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            continue
        # Save products not found every 10 messages just to reduce IO
        if count % 10 == 0:
            save_products_not_found()
