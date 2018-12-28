import pytest
from update import get_oauth_token, get_auction_data, get_auction_data_status

class TestGetOauthToken(object):
    blizz_api_url = 'https://us.battle.net/oauth/token'
    def test_incorrect_types(self):
        with pytest.raises(TypeError):
            get_oauth_token(1, 1)
            get_oauth_token(1, 1, 1)
            get_oauth_token(1, 'a', 'a')
            get_oauth_token('a', 1, 'a')
            get_oauth_token('a', 'a', 1)

    def test_http_errors(self):
        with pytest.raises(ValueError):
            get_oauth_token('a', 'a', self.blizz_api_url)
            get_oauth_token('a', 'a')

    def test_incorrect_url(self):
        with pytest.raises(ConnectionError):
            get_oauth_token('a', 'a', 'http://asd.asd')

class TestGetLastModified(object):
    def test_incorrect_types(self):
         with pytest.raises(TypeError):
            get_auction_data_status(1, 1, 1)
            get_auction_data_status(1, 1, 1, 1)
            get_auction_data_status(1, 'a', 'a', 'a')
            get_auction_data_status('a', 1, 'a', 'a')
            get_auction_data_status('a', 'a', 1, 'a')
            get_auction_data_status('a', 'a', 'a', 1)

    def test_incorrect_url(self):
        with pytest.raises(ConnectionError):
            get_auction_data_status('a', 'a', 'a', 'http://asd.asd')

class TestGetAuctionData(object):
    def test_incorrect_types(self):
         with pytest.raises(TypeError):
            get_auction_data(1)
    
    def test_incorrect_url(self):
        with pytest.raises(ConnectionError):
            get_auction_data('http://asd.asd')