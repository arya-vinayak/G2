import requests
import json
import logging
from time import sleep
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_products(url, headers, output_file):
    try_count = 0
    first_item = True  # Flag to track the first item

    while True:
        try:
            logging.info(f"Fetching data from: {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            data = response.json()

            with open(output_file, 'a') as f:
                if first_item:
                    f.write("[")
                    first_item = False

                for item in data['data']:
                    product_info = {
                        'id': item['id'],
                        'product_type': item['attributes']['product_type'],
                        'name': item['attributes']['name'],
                        'domain': item['attributes']['domain'],
                        'slug': item['attributes']['slug'],
                        'description': item['attributes']['description']
                    }

                    if first_item:
                        json.dump(product_info, f)
                    else:
                        f.write(",\n")
                        json.dump(product_info, f)

                url = data['links'].get('next')
                if url:
                    logging.info(f"Next page URL: {url}")
                else:
                    f.write("]")
                    logging.info("All data fetched. Writing to file completed.")
                    return

            try_count = 0  # Reset try count if successful

        except requests.RequestException as e:
            logging.error(f"Request failed: {e}")
            try_count += 1
            if try_count <= 1:
                logging.info(f"Retrying in 5 seconds... (Retry attempt: {try_count})")
                sleep(5)
            else:
                logging.error("Maximum retry attempts reached. Exiting...")
                break

        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            try_count += 1
            if try_count <= 1:
                logging.info(f"Retrying in 5 seconds... (Retry attempt: {try_count})")
                sleep(5)
            else:
                logging.error("Maximum retry attempts reached. Exiting...")
                break

import os  # Import the os module

def main():
    url = "https://data.g2.com/api/v1/products/"
    headers = {
        'Authorization': f"Bearer {os.environ.get('BEARER_TOKEN')}",  # Use f-string to access environment variable
        'Cookie': '__cf_bm=qwyP57KQmhMAaVag5ZEQ.6PdJyNvL9XMNVqKqoN66GQ-1712915071-1.0.1.1-vP7EaN6WHvcT.arBps6QPHhhCb0b56AnIkmplyUC9VQKdVbiZtw6GdJDR8F6Tr15jWFHE6u.d3Y7cSYqG.rsOQ; AWSALB=MYFF2ANzSWES6zaUQd6mrU2mHdi7FC6EXczHbynbm68nhTvKl20eGwXDFPVWL7cJoVcYDfflleJ7HhXB1zHlK6KgPchWPF29+LsBegLWOr+KvlOsdvT2Du2go/Pp; AWSALBCORS=MYFF2ANzSWES6zaUQd6mrU2mHdi7FC6EXczHbynbm68nhTvKl20eGwXDFPVWL7cJoVcYDfflleJ7HhXB1zHlK6KgPchWPF29+LsBegLWOr+KvlOsdvT2Du2go/Pp'
    }

    output_file = 'G2_Products.json'

    logging.info("Fetching products...")
    fetch_products(url, headers, output_file)
    logging.info("Script execution complete.")

if __name__ == "__main__":
    main()