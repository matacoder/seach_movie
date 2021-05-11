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


@dataclass
class Movie:
    locations: list
    picture: str
    name: str


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
            return self._convert_to_movies(response)

    @staticmethod
    def _convert_to_movies(response):
        results = response.json().get('results')
        movies = []
        if results:
            for title in results:
                movie = Movie(
                    [item.get('display_name') for item in
                     title.get('locations')],
                    title.get('picture'),
                    title.get('name'),
                )
                movies.append(movie)
        return movies


def search_tv_show_by_name(term='Star Trek'):
    """
    Perform search in movie database.

    ARG 1 = search term
    """
    client = RestClient(SERVER, ENDPOINT, TOKEN)
    movies = client.search_term(term)

    for title in movies:
        where_to_watch = ', '.join(title.locations)
        print(f"{title.name}, available here: ({where_to_watch})")


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
