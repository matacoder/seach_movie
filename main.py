import json
import os
from dataclasses import dataclass
from types import SimpleNamespace

import fire
import requests
from dotenv import load_dotenv
from requests import RequestException

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')


class Movie:
    """Movie object."""

    def __init__(self, **kwargs):
        """Accept all JSON fields."""
        self.__dict__.update(kwargs)


class RestClient:
    def __init__(self, server, token):
        self.server = server
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self):
        return {'X-AppKey': self.token}

    def _get_response(self, endpoint, **params):
        try:
            response = requests.get(
                self.server + endpoint,
                params=params,
                headers=self.headers
            )
            return response
        except RequestException as e:
            print(e)

    @staticmethod
    def _response_code_is_valid(response):
        return response.json().get('status_code') == 200

    def lookup_movie(self, term, endpoint='/lookup'):
        response = self._get_response(endpoint, term=term)
        if self._response_code_is_valid(response):
            return self._convert_to_movies(response)

    @staticmethod
    def _convert_to_movies(response):
        data = json.loads(response.text,
                          object_hook=lambda d: SimpleNamespace(**d))
        movies = []
        if data.results:
            for title in data.results:
                movie = Movie(
                    locations=[item.display_name for item in title.locations],
                    picture=title.picture, name=title.name
                )
                movies.append(movie)
        return movies


def search_tv_show_by_name(term='Star Trek'):
    """
    Perform search in movie database.

    ARG 1 = search term
    """
    client = RestClient(server=SERVER, token=TOKEN)
    movies = client.lookup_movie(term, endpoint='/lookup')

    for title in movies:
        where_to_watch = ', '.join(title.locations)
        print(f"{title.name}, available here: ({where_to_watch})")


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
