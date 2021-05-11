import json
import os
from dataclasses import dataclass, field

import fire
import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')
ENDPOINT = '/lookup'


class RestClient:
    def __init__(self, server, endpoint, token):
        self.server = server
        self.endpoint = endpoint
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self):
        return {'X-AppKey': self.token}

    def _get_response(self, **params):
        try:
            response = requests.get(
                self.server + self.endpoint,
                params=params,
                headers=self.headers
            )
            return response
        except RequestException as e:
            print(e)

    @staticmethod
    def _response_code_is_valid(response):
        return response.json().get('status_code') == 200

    def search_term(self, term):
        response = self._get_response(term=term)
        if self._response_code_is_valid(response):
            return response


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
                where_to_watch = ', '.join(
                    [item.get('display_name') for item in
                     title.get('locations')])
                print(
                    f"{title.get('name')}, available here: ({where_to_watch})")
    else:
        print('Attempt unsuccessful.')


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
