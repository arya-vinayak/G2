# VectorBlaze 🔥

### We implement a Innovative Cron-Job Website Scrapper with continuous streaming to the Backend Product Analytics part with G2 that blazingly processess 1000+ different products in less than 10 seconds.
### We have Focused on Fast Web scrapping and Blazing analysis of the product leveraging tools like Redis Vector Database , Vector similarity indexing and FastAPI Interaction 

## Architecture 🗺️

![image](https://github.com/arya-vinayak/G2/assets/94037471/a628c09d-5a80-4bf0-b425-bd0bf742efe2)


## Key Features 🔑

- *Web Scraping with Selenium*: Utilizes Selenium to scrape data from websites, ensuring compatibility with dynamic web pages.
- *Data Analysis and Indexing*: Employs similarity indexing to quickly check if scraped data already exists in the database.
- *Vector Database*: Utilizes the power of Vector Database for efficient data storage and retrieval, enhanced by **custom queries** and a **neural engine** for faster search.
- *Streamlit Frontend*: Offers a user-friendly interface for visualizing products not present in the database, enhancing user interaction and data exploration.

## Performance Highlights 🏎

- *Speed*: Processes over 1000+ products in just 10 seconds, showcasing the framework's high-speed capabilities.
- *Efficiency*: Utilizes similarity indexing to quickly identify existing data, reducing unnecessary processing.
- *Scalability*: Designed with scalability in mind, allowing for easy expansion and integration of new features.

## Prerequisites 😎

- Python 3.6+
- Redis Stack (local or cloud-based)
- Selenium WebDriver
- qdrant vector db
- Drive to have fun!


## Run Locally - start cookin... 💻

## **Setting Up Redis Stack Container**

To start a Redis Stack container using the **`redis-stack`** image, follow these steps:

1. Run the following command in your terminal:

```bash
docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

```

This command launches a Redis Stack container and exposes RedisInsight on port 8001. You can access RedisInsight by opening your browser and navigating to **`localhost:8001`**.

---

## **Setting Up Qdrant**

To set up Qdrant, follow these steps:

1. Download the Qdrant image from DockerHub:

```bash
docker pull qdrant/qdrant

```

2. Start Qdrant inside Docker with the following command:

```bash
docker run -p 6333:6333 \
  -v $(pwd)/qdrant_storage:/qdrant/storage \
  qdrant/qdrant

```

Once Qdrant is running, you can access its Web UI by navigating to **`localhost:6333/dashboard`**.

---

## **Setting Up Environment Variables**

Before proceeding further, create a **`.env`** file in your project directory and add the following line:

```makefile
BEARER_TOKEN=your_bearer_token_here

```

Replace **`your_bearer_token_here`** with your actual bearer token.

---

## **Generating Data**

Now, generate the required data by following these steps:

1. Run the **`ProductsCollector.py`** script to create **`G2_Products.json`**.
2. Pre-process **`G2_Products.json`** to produce **`G2_Cleaned.json`**.

---

## **Building the Neural Search Engine**

To build the neural search engine, follow these steps:

1. Open the **`Qdrant_store.ipynb`** notebook.
2. Sequentially run the cells in the notebook to vectorize the G2 Products data and prepare the neural search engine.

---

## **Running the Processor**

Once everything is set up, run the **`processor.py`** script to perform high-speed processing:

```bash
python processor.py

```

This script will handle the heavy lifting tasks.

---
## **Running Selenium Web Scraper**

To set up and run the Selenium web scraper, setup the container:

```bash
docker run -d -p 4000:4444 -v /dev/shm:/dev/shm selenium/standalone-chrome
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
  
Now your environment should be set up and ready to go! If you encounter any issues, feel free to reach out for assistance.

## References 🌐
- [QDrant Neural Search](https://qdrant.tech/documentation/tutorials/neural-search/)
- [Selenium Docs](https://www.selenium.dev/documentation/)
- [Redis Pub/Sub](https://redis.io/glossary/pub-sub/#:~:text=Python%20Redis%20Pub%2FSub&text=Python%20can%20be%20used%20to,sub%20messaging%20in%20Python%20applications.)
