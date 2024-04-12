#!/usr/bin/env python3

import logging
import time
import json
import redis
import schedule
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

redis_host = "localhost"
redis_port = 6379
redis_client = redis.Redis(host=redis_host, port=redis_port)
channel_name = "newProductsSourceForge"

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Remote(command_executor='http://localhost:4000/wd/hub', options=options)

fetched_products = []

def produce_data(channel_name, products):
    for product in products:
        newProduct = {
            "name": product["title"],
            "description": product["description"],
        }
        redis_client.publish(channel_name, json.dumps(newProduct))
    logging.info("Data sent to redis!")

def getProductsFromPage(category):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul.projects")))
    projects_list = driver.find_element(By.CSS_SELECTOR, "ul.projects")
    for project in projects_list.find_elements(By.TAG_NAME, "li"):
        try:
            if project.get_attribute("class") == "project-oss":
                title = project.find_element(By.CSS_SELECTOR, "div.result-heading-texts > div.title-subtitle-wrapper > div > a > h3").text.strip()
                description = project.find_element(By.CSS_SELECTOR, "div.description").text.strip()
                product_link = project.find_element(By.CSS_SELECTOR, "div.result-heading-texts > div.title-subtitle-wrapper > div > a").get_attribute("href")
            else:
                title = project.find_element(By.CSS_SELECTOR, "div.heading-main > a").text.strip()
                description = project.find_element(By.CSS_SELECTOR, "div.description-inner").text.strip()
                product_link = project.find_element(By.CSS_SELECTOR, "div.heading-main > a").get_attribute("href")
        except Exception as e:
            logging.error("Error while fetching data from page!")
            logging.error(e)
            continue
        print("Title:", title)
        print("Description:", description)
        print("Product Link:", product_link, end="\n\n")
        print("Category:", category)
        fetched_products.append({
            "title": title if title else "NA",
            "description": description if description else "NA",
            "product_link": product_link if product_link else "NA",
            "raw_text": project.text,
            "category": category
        })
    produce_data(channel_name, fetched_products)

def main():
    global driver
    global fetched_products
    categories = ["windows", "linux", "software-development", "mac", "system", "multimedia", "games"]
    logging.info("Fetching data from SourceForge started!")
    for category in categories:
        driver.get(f"https://sourceforge.net/directory/{category}/?sort=update")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content")))
        for _ in range(4):
            getProductsFromPage(category)
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next")
            next_button.click()
        except Exception as e:
            logging.warning("No more pages to fetch!")
            continue
    # driver.quit()
    logging.info("Driver closed!")
    logging.info("Fetching data completed!")
    logging.info(f"Size of fetched products: {len(fetched_products)}")
    with open(f"sourceforge_products_{time.time()}.json", "w") as f:
        json.dump(fetched_products, f, indent=4)
        fetched_products.clear()
    logging.info("Data saved to file!")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting the script!")
    # main()
    schedule.every().minute.do(main)
    while True:
        schedule.run_pending()
        time.sleep(10)