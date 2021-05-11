import json
import os

import fire
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')


def search_tv_show_by_name(term='Star Trek', display='human'):
    """
    Perform search in movie database.

    ARG 1 = search term
    ARG 2 = display view (human or json)
    """
    headers = {
        'X-AppKey': TOKEN,
    }
    params = {
        'term': term,
    }
    r = requests.get(SERVER + '/lookup', params=params, headers=headers)
    if display == 'json':
        parsed = json.loads(r.text)
        print(json.dumps(parsed, indent=4, sort_keys=True))
    else:
        for title in r.json().get('results'):
            where_to_watch = ', '.join([item.get('display_name') for item in title.get('locations')])
            print(f"{title.get('name')}, available here: ({where_to_watch})")


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
