# VectorBlaze 🔥

### We implement a Innovative Cron-Job Website Scrapper with continuous streaming to the Backend Product Analytics part with G2 that blazingly processess 1000+ different products in less than 10 seconds.
### We have Focused on Fast Web scrapping and Blazing analysis of the product leveraging tools like Redis Vector Database , Vector similarity indexing and FastAPI Interaction 

## Architecture 🗺️

![image](https://github.com/arya-vinayak/G2/assets/94037471/a628c09d-5a80-4bf0-b425-bd0bf742efe2)

## Run Locally 💻
- installations
```bash
# docker containers
docker run -d -p 6379:6379 redis
docker run -d -p 4000:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
docker run -p 6333:6333 -v $(pwd)/qdrant_storage:/qdrant/storage qdrant/qdrant
```

- installing python libraries
```bash
pip install -r requirements.txt
```
- run selenium web scraper
```bash
python3 scraper/fetchSourceForge.py
```
- visit `http://localhost:4000/` to see scraper in action
- 

## References 🌐
- [QDrant Neural Search](https://qdrant.tech/documentation/tutorials/neural-search/)
- [Selenium Docs](https://www.selenium.dev/documentation/)
- [Redis Pub/Sub](https://redis.io/glossary/pub-sub/#:~:text=Python%20Redis%20Pub%2FSub&text=Python%20can%20be%20used%20to,sub%20messaging%20in%20Python%20applications.)
