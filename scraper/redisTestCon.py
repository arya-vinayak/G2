import redis

redis_host = "localhost"
redis_port = 6379

redis_client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

channel = "newProductsSourceForge"
consumer = redis_client.pubsub()
consumer.subscribe(channel)
            
for message in consumer.listen():
    print(message)