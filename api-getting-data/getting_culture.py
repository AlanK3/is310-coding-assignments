import requests
import csv
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
EUROPEANA_API_KEY = os.getenv("EUROPEANA_API_KEY")

def fetch_data(query):
    base_url = "https://api.europeana.eu/record/v2/search.json"
    params = {
        'wskey': EUROPEANA_API_KEY,
        'query': query,
        'rows': 5
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)
        return None

def extract_item_info(data):
    if data and 'items' in data:
        item = data['items'][0]
        print("Item details:", item)
        return item
    else:
        print("No items found in the data.")
        return None

def save_to_csv(item_data, filename="europeana_data.csv"):
    headers = ["title", "creator", "date", "type", "link"]
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        writer.writerow({
            "title": item_data.get("title", ["N/A"])[0] if item_data.get("title") else "N/A",
            "creator": item_data.get("dcCreator", ["N/A"])[0] if item_data.get("dcCreator") else "N/A",
            "date": item_data.get("year", "N/A"),
            "type": item_data.get("type", "N/A"),
            "link": item_data.get("guid", "N/A")
        })
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    data = fetch_data("Van Gogh")
    item = extract_item_info(data)
    if item:
        save_to_csv(item)