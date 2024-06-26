import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://login-b2b-ats-healthcare.us.auth0.com"


def save_response(response, file_name):
    response.raise_for_status()
    response_data = response.json()
    with open(f"{file_name}.json", "w") as json_file:
        json.dump(response_data, json_file, indent=4)


def read_json(file_path):
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_token():
    token_url = f"{url}/oauth/token"
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "audience": "https://test.api.ats.healthcare",
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(token_url, json=data, headers=headers)
    save_response(response, "token")


def request_pickup():
    pickup_url = f"{url}/v1/PickupRequests"
    data = {
        "pickupTime": "string",
        "closingTime": "string",
        "pieces": 0,
        "weight": 0,
        "email": "string",
        "saveEmailAsDefault": False,
    }
    token_json = read_json("token.json")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {token_json["access_token"]}",
    }

    response = requests.post(pickup_url, json=data, headers=headers)
    save_response(response, "pickup")


if __name__ == "__main__":
    get_token()
    # request_pickup()
