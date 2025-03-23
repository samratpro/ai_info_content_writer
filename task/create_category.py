import httpx
import requests
import json
from models import Postdata, Session
import base64

def create_category():
    category_id = None
    session = Session()
    settings = session.query(Postdata).filter_by(id=1).first()
    if settings:
        cat_name = settings.category_name
        website = settings.website_name
        username = settings.username
        app_pass = settings.app_pass
        credentials = f"{username}:{app_pass}"
        encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
        headers = {"Authorization": f"Basic {encoded_credentials}", }

        data = {"name": cat_name}
        try:
            # Attempt to create category by posting data to WP
            cat = httpx.post(website + 'wp-json/wp/v2/categories', headers=headers, json=data, timeout=30)
            cat.raise_for_status()  # Raise an exception for HTTP errors
            cat_json = cat.json()

            # Check if the category was successfully created and retrieve its ID
            if 'id' in cat_json:
                category_id = cat_json['id']
            elif 'message' in cat_json and cat_json['message'] == "Category already exists":
                # If the category already exists, retrieve its ID from existing categories
                cat = httpx.get(website + 'wp-json/wp/v2/categories', headers=headers)
                cat.raise_for_status()  # Raise an exception for HTTP errors
                cat_list = cat.json()
                for existing_cat in cat_list:
                    if cat_name.lower() == existing_cat['name'].lower():
                        category_id = existing_cat['id']
                        break  # Exit the loop once the category is found
        except httpx.ConnectError as e:
            print(f"Connection error: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except httpx.RequestError as e:
            print(f"Request error: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except KeyError:
            # Catch any unexpected errors (e.g., missing fields in the response)
            print("Unexpected error occurred while processing category.")
    # Ensure category_id is of type integer
    if category_id is not None:
        return int(category_id)
    return None