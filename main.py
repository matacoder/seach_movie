import logging
import os

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
        """Accept all dict fields as properties."""
        self.__dict__.update(kwargs)

    def get_locations(self):
        """Return comma separated string of Video Services."""
        return ', '.join(
            [location['display_name'] for location in self.locations]
        )


class RestClient:
    """Connect to server with token."""

    def __init__(self, server, token):
        self.server = server
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self):
        """Build headers for authentication."""
        return {'X-AppKey': self.token}

    def _get_response(self, endpoint, **params):
        """Get response object from custom endpoint."""
        try:
            response = requests.get(
                self.server + endpoint,
                params=params,
                headers=self.headers
            )
            return response
        except RequestException as e:
            logging.error(e)

    @staticmethod
    def _response_code_is_valid(response):
        return response.json().get('status_code')

    def lookup_movies(self, term, endpoint='/lookup'):
        """Returns list of movies objects according search term."""
        response = self._get_response(endpoint, term=term)
        if response is not None:
            status_code = self._response_code_is_valid(response)
            if status_code == 200:
                return self._convert_to_movies_2(response)
            else:
                logging.error(f'API status code is {status_code}')
        else:
            logging.error(f'No response at all. Check server endpoint.')

    @staticmethod
    def _convert_to_movies_2(response):
        """Keep movies as object to simplify properties lookup."""
        movies = []
        data = response.json().get('results')
        if data:
            for item in data:
                movies.append(Movie(**item))
        else:
            logging.info('Response has no "results" section.')
        return movies


def search_tv_show_by_name(term='Star Trek'):
    """
    Perform search in movie database.

    ARG 1 = search term
    """
    client = RestClient(server=SERVER, token=TOKEN)
    movies = client.lookup_movies(term, endpoint='/lookup')
    if movies:
        for title in movies:
            print(
                f"{title.name}, available here: {title.get_locations()}")
    else:
        print("No results found.")


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
