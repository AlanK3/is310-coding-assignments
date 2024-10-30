import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment
MTD_API_KEY = os.getenv("MTD_API_KEY")  # keys are hidden in the hidden .env file

def fetch_data():
    base_url = "https://developer.mtd.org/api/v2.2/json/getvehicles"
    params = {
        'key': "MTD_API_KEY",
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Failed to retrieve data:", response.status_code)
        return None
    
def save_to_json(data, filename="mtd_vehicle_data.json"):
    # Save the data to a JSON file
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    # Fetch vehicle data and save to JSON if data retrieval was successful
    vehicle_data = fetch_data()
    if vehicle_data:
        save_to_json(vehicle_data)