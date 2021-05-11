import unittest

import requests

from main import TOKEN, SERVER


class TestAPI(unittest.TestCase):

    def test_api_key(self):
        headers = {
            'X-AppKey': TOKEN,
        }
        params = {
            'term': 'Star Trek',
        }
        r = requests.get(SERVER + '/lookup', params=params, headers=headers)
        self.assertEqual(r.json().get('status_code'), 200)


if __name__ == '__main__':
    unittest.main()
