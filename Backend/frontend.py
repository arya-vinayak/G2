import streamlit as st
import pandas as pd
import json
import redis
import schedule
import time

# Load the JSON data from a local file
with open('products_not_found.json', 'r') as f:
    data = json.load(f)

# Convert the JSON data to a pandas DataFrame
df = pd.DataFrame(data)

# Redis setup
r = redis.Redis(host='localhost', port=6379, db=0)
p = r.pubsub()

# Function to refresh the data
def load_data():
    return df

# Function to scrape other websites and update the header
def scrape_and_update_header():
    # Your scraping logic here
    # Update header with the latest information
    latest_info = "Latest information from scraping other websites"
    st.header(latest_info)

# Schedule the scraping job to run periodically
schedule.every(1).day.do(scrape_and_update_header)  # Adjust frequency as needed

# Streamlit app
def app():
    # Sidebar with navigation
    pages = {
        "Home": home_page,
        "Table": table_page,
        "Redis Pub/Sub": redis_page
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Call the selected page function
    pages[selection]()


def home_page():
    st.title("Welcome to Our Website!")
    st.write("Our website offers a comprehensive solution for identifying new Google Analytics (GA) products and comparing them with products listed on G2.")

    st.header("Components:")
    st.subheader("1. Periodic New GA Products Identification Component:")
    st.write("Responsible for identifying new GA products through various sources such as industry news, product launch announcements, etc.")

    st.subheader("2. G2 API Integration:")
    st.write("Interacts with the G2 API to retrieve the list of currently listed products on G2 and the new GA products identified by the previous component.")

    st.subheader("3. Data Processing and Comparison Component:")
    st.write("Compares the list of new GA products with the products currently listed on G2 to identify any products that are not yet listed.")

    st.subheader("4. Output Generation Component:")
    st.write("Generates the final output, which includes:")
    st.markdown("- A list of new GA products not listed on G2.")
    st.markdown("- Popularity scores for each product.")
    st.write("Stores the output in a database or exports it to a CSV file for further processing.")

    st.header("5. Cron Job Scheduling:")
    st.write("Periodically scrapes the web for new product information defined as a cron job and updates the listy accordingly.")

    st.info("Feel free to navigate through the different pages using the sidebar.")

def table_page():
    st.title("App Names")
    data = load_data()
    st.table(data[['name']])

def redis_page():
    st.title("Redis Pub/Sub")
    subscribe_channel = st.text_input("Enter channel to subscribe", "my-channel")
    if st.button("Subscribe"):
        p.subscribe(subscribe_channel)
        st.write(f"Subscribed to {subscribe_channel}")

    for message in p.listen():
        if message['type'] == 'message':
            try:
                data = json.loads(message['data'])
                st.write(f"Scraped product: {data.get('name')}")
            except Exception as e:
                print(f"Error processing message: {str(e)}")
                continue

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)  # Adjust sleep time as needed
