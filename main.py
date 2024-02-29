import requests
import json
from db import get_redis_connection

#Connect to RedisDB
r = get_redis_connection()

#Get API
api_url = "https://jsonplaceholder.typicode.com/posts"

class JSONgrabber:
    """A class to fetch JSON data from an API and store it in RedisJSON DB."""

    def __init__(self, api_url):
        """
        Initialize the class with the API URL.

        Args:
            api_url (str): The URL of the API.
        """
        self.api_url = api_url
        self.redis_conn = get_redis_connection()

    def fetch_data_from_api(self):
        """Fetch JSON data from the API."""
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data from API: {response.status_code}")

    def store_data_in_redis(self, data):
        """Store JSON data in RedisJSON."""
        for item in data:
            key = f'post:{item["id"]}'
            self.redis_conn.json().set(key, '.', json.dumps(item))

class JSONretrieval:
    """This class retrieves JSON from the Redis DB and conducts some short work."""

    keys = ['userId', 'id', 'title', 'body']

    def __init__(self):
        print("Retrieving JSON")

    def fetch_JSON(self):
        JSON_data = r.json().get('post')


#Grabs and stores JSON from the API into a RedisJSONdb. 
if __name__ == "__main__":

    processor = JSONgrabber(api_url)
    json_data = processor.fetch_data_from_api()
    processor.store_data_in_redis(json_data)