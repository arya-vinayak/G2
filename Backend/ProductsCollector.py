# Import necessary libraries
import requests  # For making HTTP requests
import json  # For handling JSON data
import logging  # For logging messages
from time import sleep  # For adding delays
import os  # For accessing environment variables and performing file operations

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch products from API and store them in a JSON file
def fetch_products(url, headers, output_file):
    try_count = 0
    first_item = True  # Flag to track the first item

    while True:
        try:
            # Log information about fetching data
            logging.info(f"Fetching data from: {url}")

            # Send GET request to the API endpoint
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            # Parse the JSON response
            data = response.json()

            # Open the output file for appending
            with open(output_file, 'a') as f:
                if first_item:
                    f.write("[")  # Start writing JSON array
                    first_item = False

                # Iterate over each item in the response data
                for item in data['data']:
                    # Extract relevant product information
                    product_info = {
                        'id': item['id'],
                        'product_type': item['attributes']['product_type'],
                        'name': item['attributes']['name'],
                        'domain': item['attributes']['domain'],
                        'slug': item['attributes']['slug'],
                        'description': item['attributes']['description']
                    }

                    # Write product information to the JSON file
                    if first_item:
                        json.dump(product_info, f)
                    else:
                        f.write(",\n")
                        json.dump(product_info, f)

                # Get URL for the next page of data
                url = data['links'].get('next')
                if url:
                    logging.info(f"Next page URL: {url}")
                else:
                    f.write("]")  # End writing JSON array
                    logging.info("All data fetched. Writing to file completed.")
                    return

            try_count = 0  # Reset try count if successful

        except requests.RequestException as e:
            # Log error if request fails
            logging.error(f"Request failed: {e}")
            try_count += 1
            if try_count <= 1:
                logging.info(f"Retrying in 5 seconds... (Retry attempt: {try_count})")
                sleep(5)
            else:
                logging.error("Maximum retry attempts reached. Exiting...")
                break

        except json.JSONDecodeError as e:
            # Log error if JSON decoding fails
            logging.error(f"JSON decode error: {e}")
            try_count += 1
            if try_count <= 1:
                logging.info(f"Retrying in 5 seconds... (Retry attempt: {try_count})")
                sleep(5)
            else:
                logging.error("Maximum retry attempts reached. Exiting...")
                break

# Main function to execute the script
def main():
    # URL of the API endpoint
    url = "https://data.g2.com/api/v1/products/"

    # Headers including authorization token
    headers = {
        'Authorization': f"Bearer {os.environ.get('BEARER_TOKEN')}",  # Use f-string to access environment variable
        'Cookie': '__cf_bm=qwyP57KQmhMAaVag5ZEQ.6PdJyNvL9XMNVqKqoN66GQ-1712915071-1.0.1.1-vP7EaN6WHvcT.arBps6QPHhhCb0b56AnIkmplyUC9VQKdVbiZtw6GdJDR8F6Tr15jWFHE6u.d3Y7cSYqG.rsOQ; AWSALB=MYFF2ANzSWES6zaUQd6mrU2mHdi7FC6EXczHbynbm68nhTvKl20eGwXDFPVWL7cJoVcYDfflleJ7HhXB1zHlK6KgPchWPF29+LsBegLWOr+KvlOsdvT2Du2go/Pp; AWSALBCORS=MYFF2ANzSWES6zaUQd6mrU2mHdi7FC6EXczHbynbm68nhTvKl20eGwXDFPVWL7cJoVcYDfflleJ7HhXB1zHlK6KgPchWPF29+LsBegLWOr+KvlOsdvT2Du2go/Pp'
    }

    # Output file name
    output_file = 'G2_Products.json'

    # Log information about fetching products
    logging.info("Fetching products...")

    # Call fetch_products function to fetch and store products
    fetch_products(url, headers, output_file)

    # Log completion of script execution
    logging.info("Script execution complete.")

# Entry point of the script
if __name__ == "__main__":
    main()
