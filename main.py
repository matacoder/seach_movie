import json
import os

from dotenv import load_dotenv
import requests

load_dotenv()

TOKEN = os.getenv('TOKEN')
SERVER = os.getenv('SERVER')


def search_tv_show_by_name(term):
    headers = {
        'X-AppKey': TOKEN,
    }
    params = {
        'term': term,
    }
    r = requests.get(SERVER + '/lookup', params=params, headers=headers)
    parsed = json.loads(r.text)
    print(json.dumps(parsed, indent=4, sort_keys=True))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    search_tv_show_by_name('Star Trek')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
