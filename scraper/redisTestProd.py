import redis
import json

redis_host = "localhost"
redis_port = 6379

redis_client = redis.Redis(host=redis_host, port=redis_port)

steam_name = "newProductsSourceForge"

def produce_data(stream_name, product):
    product = redis_client.publish(stream_name, json.dumps(product)) 
    print(product)

with open("products.json", "r") as file:
    data = json.load(file)
    for product in data:
        produce_data(steam_name, product)    

