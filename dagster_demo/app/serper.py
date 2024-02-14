import os
import pandas as pd
from datetime import datetime
import requests
import json
from ..utils import read_json, write_json


class Serper:
    search_data_folder = 'data/search_data'

    def __init__(self, api_key):
        os.makedirs(self.search_data_folder, exist_ok=True)
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

    def get_new_search_results(self, client_name, competitors_list):
        filename = f'{self.search_data_folder}/{client_name}.json'
        previous_data = read_json(filename)
        if not previous_data:
            previous_data = {c: {} for c in competitors_list}
        new_results = self.search(competitors_list)
        time_now = str(datetime.now())
        convert_dict = lambda x: {i['link']: {'title': i.get('title'), 'date': time_now,  'snippet': i.get('snippet')} for i in x}
        current_data = {c: convert_dict(res.get('organic', [])) for c, res in zip(competitors_list, new_results)}

        new_data = {c: {link: info for link, info in links.items() if link not in previous_data.get(c, {})} for c, links in current_data.items()}
        all_data = {c: {**previous_data.get(c, {}), **links} for c, links in current_data.items()}
        write_json(filename, all_data)
        return self._convert_to_df(new_data, client_name)

    def _convert_to_df(self, new_data, client_name):
        rows = []
        for company, links in new_data.items():
            for link, info in links.items():
                info['url'] = link
                rows.append(info)

        df = pd.DataFrame(rows)
        df['company_name'] = client_name
        return df
