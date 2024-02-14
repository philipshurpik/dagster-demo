import requests
import json


class Serper:
    def __init__(self, api_key):
        self.url = "https://google.serper.dev/search"
        self.headers = {
            'X-API-KEY': api_key,
            'Content-Type': 'application/json'
        }

    def search(self, requests_list):
        queries = [{"q": r} for r in requests_list]
        payload = json.dumps(queries)
        response = requests.request("POST", self.url, headers=self.headers, data=payload)
        return json.loads(response.text)
