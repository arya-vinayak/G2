from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from neural_searcher import NeuralSearcher
import redis
import json

r = redis.Redis(
    host='127.0.0.1',
    port=6379,
    decode_responses=True
)
print("connected to redis")

# pubsub() method creates the pubsub object
# but why i named it mobile 🧐
# just kidding 😂 think of it as the waki taki that listens for incomming messages
mobile = r.pubsub()
mobile.subscribe('newProductsSourceForge')


# Load a pre-trained model for encoding text into vectors as well as the Neural Searcher for Superfact Search
model = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")
print("Model loaded successfully")
Products_Not_Exist = []
neural_searcher = NeuralSearcher("G2products")
print("Neural Searcher loaded successfully")


def cosine_similarity_between_strings(string1, string2): 
    # Encode the input strings into vectors
    vector1 = model.encode(string1)
    vector2 = model.encode(string2)

    # Reshape the vectors for cosine similarity calculation
    vector1 = vector1.reshape(1, -1)
    vector2 = vector2.reshape(1, -1)

    # Calculate cosine similarity between the two vectors
    similarity_score = cosine_similarity(vector1, vector2)[0][0]

    return similarity_score

def get_similar_products(product_name, filter=None):
    # Search for similar products based on the product name
    similar_products = neural_searcher.search(product_name, filter)
    return similar_products

def get_similarity_score(product1, product2):
    if(product1["name"] == product2["name"]):
        return 1.0
    if(product1["description"] == None):
        return 0.0

    similarity_score_names = cosine_similarity_between_strings(product1["name"], product2["name"])
    similarity_score_descriptions = cosine_similarity_between_strings(product1["description"], product2["description"])
    similarity_score =  0.6 * similarity_score_names + 0.4 * similarity_score_descriptions

    return similarity_score


def process_product(product):
    # Get similar products based on the product name
    similar_products = get_similar_products(product["name"])
    # Calculate similarity scores with each similar product
    similarity_score = get_similarity_score(product, similar_products[0])
    if similarity_score > 0.85:
        # ignore the product itself
        print("Product already exists")
    else :
        # add product to the products not found list
        print("Product not found")
        Products_Not_Exist.append(product)


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
        if count%10 == 0:
            save_products_not_found()



