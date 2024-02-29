import requests
import json
import redis
from db import get_redis_connection

#Connect to RedisDB
r = get_redis_connection()
#Get API
api_url = "https://jsonplaceholder.typicode.com/posts"

class apiData:
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
    """A class to retrieve JSON data from RedisJSON."""

    def __init__(self):
        """Initialize the class."""
        self.redis_conn = get_redis_connection()

    def get_data_from_redis(self, keys):
        """Retrieve JSON data from RedisJSON."""
        json_data = {}
        for key in keys:
            json_data[key] = self.redis_conn.json().get(key)
        return json_data