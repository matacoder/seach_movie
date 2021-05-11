import json
import os

import fire
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')


def search_tv_show_by_name(term='Star Trek'):
    headers = {
        'X-AppKey': TOKEN,
    }
    params = {
        'term': term,
    }
    r = requests.get(SERVER + '/lookup', params=params, headers=headers)
    parsed = json.loads(r.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))


if __name__ == '__main__':
    fire.Fire(search_tv_show_by_name)
