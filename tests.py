import unittest

from main import RestClient, search_tv_show_by_name


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class MockRestClient(RestClient):
    def _get_response(self, endpoint, **params):
        text = {
            'results': [{
                'id': '5d97da9e9a76a40056de50d3',
                'picture': 'https://utellyassets9-1.imgix.net/api/Images/9d3f3c80f8a2ddd041ec1804ecced01a/Redirect?fit=crop&auto=compress&crop=faces,top',
                'name': 'Star Trek: Generations', 'locations': [{
                    'icon': 'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/iTunesIVAGB.png?w=92&auto=compress&app_version=b58ebc89-0c7e-463c-b508-88b7f5958bd6_wwe42021-05-08',
                    'display_name': 'iTunes',
                    'name': 'iTunesIVAGB',
                    'id': '5d8415b3ca549f00528a99f0',
                    'url': 'https://itunes.apple.com/gb/movie/star-trek-vii-generations/id210534030'
                },
                    {
                        'icon': 'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/GooglePlayIVAGB.png?w=92&auto=compress&app_version=b58ebc89-0c7e-463c-b508-88b7f5958bd6_wwe42021-05-08',
                        'display_name': 'Google Play',
                        'name': 'GooglePlayIVAGB',
                        'id': '5d84d6dcd95dc7385f6a43e1',
                        'url': 'https://play.google.com/store/movies/details/Star_Trek_VII_Generations?gl=gb&hl=en&id=-cxqHVyEU-U'
                    },
                    {
                        'icon': 'https://utellyassets7.imgix.net/locations_icons/utelly/black_new/AmazonInstantVideoIVAGB.png?w=92&auto=compress&app_version=b58ebc89-0c7e-463c-b508-88b7f5958bd6_wwe42021-05-08',
                        'display_name': 'Amazon Instant Video',
                        'name': 'AmazonInstantVideoIVAGB',
                        'id': '5d8415b31e1521005490e1bc',
                        'url': 'https://watch.amazon.co.uk/detail?asin=B00GKW0ZWK&creativeASIN=B00GKW0ZWK&ie=UTF8&linkCode=xm2&tag=utellycom00-21'
                    }],
                'provider': 'iva', 'weight': 0, 'external_ids': {
                    'iva_rating': None, 'imdb': {
                        'url': 'https://www.imdb.com/title/tt0111280',
                        'id': 'tt0111280'
                    }, 'tmdb': {
                        'url': 'https://www.themoviedb.org/movie/193',
                        'id': '193'
                    }, 'wiki_data': {
                        'url': 'https://www.wikidata.org/wiki/Q723679',
                        'id': 'Q723679'
                    }, 'iva': {'id': '5537'}, 'gracenote': None,
                    'rotten_tomatoes': None, 'facebook': None
                }
            }], 'updated': '2021-05-08T14:07:37+0100',
            'term': 'Star Trek: Generations', 'status_code': 200,
            'variant': 'ivafull'
        }
        status_code = 200
        response = MockResponse(text, status_code)
        return response if params['term'] == 'Star Trek: Generations' else None


class TestAPI(unittest.TestCase):
    def test_movie_converter(self):
        term = 'Star Trek: Generations'
        client = MockRestClient('https://mock', 'mock_token')
        movies = client.lookup_movies(term, endpoint='/lookup')
        self.assertEqual(len(movies), 1)
        self.assertEqual(movies[0].name, 'Star Trek: Generations')

    def test_results_not_found(self):
        term = 'ThatMovieDoesNotExist'
        client = MockRestClient('https://mock', 'mock_token')
        movies = client.lookup_movies(term, endpoint='/lookup')
        self.assertEqual(movies, None)


if __name__ == '__main__':
    unittest.main()
