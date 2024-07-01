import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://login-b2b-ats-healthcare.us.auth0.com"

base = "https://atsapi-dev.azurewebsites.net"


def save_response(response, file_name):
    response_data = response.json()
    status = response.status_code
    print(status)
    if status == 204:
        return True
    main_path = f"./response_examples/{file_name}"
    file_path = f"{main_path}/{file_name}_{status}.json"
    with open(file_path, "w") as json_file:
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


def create_headers():
    token_json = read_json("token.json")
    return {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {token_json["access_token"]}",
    }


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
    pickup_url = f"{base}/v1/PickupRequests"
    data = {
        "pickupTime": "1400",
        "closingTime": "1900",
        "pieces": 2,
        "weight": 10
    }
    token_json = read_json("token.json")
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "authorization": f"Bearer {token_json["access_token"]}",
    }

    response = requests.post(pickup_url, json=data, headers=headers)
    save_response(response, "pickup")


def create_shipment():
    shipment_url = f"{base}/v1/Shipments"

    data = {
        "docketCode": "ATSDemo2",
        "address": {
            "name": "John Doe",
            "attentionTo": "Jane Doe",
            "address1": "150-18279 Blundell Rd",
            "city": "Vancouver",
            "province": "BC",
            "postalCode": "V6W1L8",
            "country": "CA",
            "isResidential": False,
        },
        "phone": '123-456-7890',
        "email": "john.doe@ats.ca",
        "pieces": 5,
        "totalWeight": 15,
        "isPallet": False,
        "instructions": "Handle with care",
        "descriptionOfGoods": "Medical supplies",
        "shipDate": "2024-07-03T10:00:00Z",
        "accessorials": ["DG"],
        "serviceCode": "GE",
        "source": "wineDirect",
        "paymentTerm": "prepaid",
    }

    headers = create_headers()

    response = requests.post(shipment_url, json=data, headers=headers)
    save_response(response, "create_shipment")


def get_shipment_labels():
    label_url = f"{base}/v1/Shipments/label?trackingNumber=900014422"

    headers = create_headers()

    response = requests.get(label_url, headers=headers)
    save_response(response, "get_labels")


def get_shipment_labels_by_id():
    label_url = f"{base}/v1/Shipments/11038/label"

    headers = create_headers()

    response = requests.get(label_url, headers=headers)
    save_response(response, "get_labels_id")


def get_continuous_manifest():
    manifest_url = f"{base}/v1/Manifests/continuous"

    headers = create_headers()

    response = requests.get(manifest_url, headers=headers)
    save_response(response, "continuous_manifest")


def add_shipment_to_manifest():
    manifest_url = f"{base}/v1/Manifests/504/shipments"

    headers = create_headers()

    data = {
        "ids": [11536]
    }

    response = requests.post(manifest_url, json=data, headers=headers)
    save_response(response, "add_to_manifest")


def close_manifest():
    manifest_url = f"{base}/v1/Manifests/504"

    headers = create_headers()

    data = {
        # "status": "closed"
    }

    response = requests.patch(manifest_url, json=data, headers=headers)
    save_response(response, "close_manifest")


if __name__ == "__main__":
    # get_token()
    # request_pickup()
    # create_shipment()
    # get_shipment_labels()
    # get_shipment_labels_by_id()
    # add_shipment_to_manifest()
    # get_continuous_manifest()
    close_manifest()
