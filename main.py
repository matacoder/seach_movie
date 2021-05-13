import logging
import os

import fire
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
SERVER = os.getenv("SERVER")


class Location:
    def __init__(self, *args, **kwargs):
        self.display_name = None
        self.__dict__.update(kwargs)


class Movie:
    """Movie object."""

    def __init__(self, *args, **kwargs):
        self._name, self.locations = None, []
        kwargs["_name"] = kwargs.pop("name", None)
        self.__dict__.update(kwargs)
        self.locations = [Location(**location) for location in self.locations]

    def get_locations(self):
        """Return comma separated string of Video Services."""
        return ", ".join([location.display_name for location in self.locations])

    @property
    def name(self):
        return self._name


class RestClient:
    """Connect to server with token."""

    def __init__(self, server, token):
        self.server = server
        self.token = token
        self.headers = self._get_headers()

    def _get_headers(self):
        """Build headers for authentication."""
        return {"X-AppKey": self.token}

    def _get_response(self, endpoint, **params):
        """Get response object from custom endpoint."""
        response = requests.get(
            self.server + endpoint, params=params, headers=self.headers
        )
        if response.status_code in [200, 201]:
            return response.json()
        else:
            logging.error(
                f"API status code is {response.status_code}\n"
                f"Server said: {response.reason}"
            )
            raise Exception("Request Failed")

    def lookup_movies(self, term, endpoint="/lookup"):
        """Returns list of movies objects according search term."""
        response = self._get_response(endpoint, term=term)
        return self._convert_to_movies_2(response)

    @staticmethod
    def _convert_to_movies_2(response):
        """Keep movies as object to simplify properties lookup."""
        for item in response.get("results", []):
            yield Movie(**item)


def search_tv_show_by_name(term="Star Trek"):
    """
    Perform search in movie database.

    ARG 1 = search term
    """
    client = RestClient(server=SERVER, token=TOKEN)
    movies = client.lookup_movies(term)
    if movies:
        for title in movies:
            yield f"{title.name}, available here: {title.get_locations()}"
    else:
        yield "No results found."


if __name__ == "__main__":
    # Using Google Fire to create simple CLI
    fire.Fire(search_tv_show_by_name)
