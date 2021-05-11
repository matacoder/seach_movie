import json
import os
from dataclasses import dataclass

import fire
import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')
ENDPOINT = '/lookup'


@dataclass
class RestClient:
    server: str
    endpoint: str
    token: str

    def search_term(self, term):
        headers = {
            'X-AppKey': self.token,
        }
        params = {
            'term': term,
        }
        try:
            r = requests.get(self.server + self.endpoint, params=params, headers=headers)
            if r.json().get('status_code') == 401:
                print(f"{r.json().get('message')}")
            else:
                return r
        except RequestException as e:
            print(e)


def search_tv_show_by_name(term='Star Trek', display='human'):
    """
    Perform search in movie database.

    ARG 1 = search term
    ARG 2 = display view (human or json)
    """
    client = RestClient(SERVER, ENDPOINT, TOKEN)
    r = client.search_term(term)
    if r is not None:
        if display == 'json':
            parsed = json.loads(r.text)
            print(json.dumps(parsed, indent=4, sort_keys=True))
        else:
            for title in r.json().get('results'):
                where_to_watch = ', '.join([item.get('display_name') for item in title.get('locations')])
                print(f"{title.get('name')}, available here: ({where_to_watch})")
    else:
        print('Attempt unsuccessful.')


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
