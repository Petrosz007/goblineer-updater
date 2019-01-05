import pytest, sys
sys.path.insert(0, '')
from src.update import get_oauth_token, get_auction_data, get_auction_data_status, parse_auctions

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

class TestParseAuctions(object):
    def test_incorrect_types(self):
        with pytest.raises(TypeError):
            parse_auctions({'a': 1})
            parse_auctions(1)

    def test_correct_value(self):
        test0 = []
        assert {} == parse_auctions(test0)

        test1 = [
            {'item': 1, 'buyout': 0, 'quantity': 10},
            {'item': 1, 'buyout': 10000, 'quantity': 1}
        ]
        assert {(1,): {1: 1}} == parse_auctions(test1)

        test2 = [
            {'item': 1, 'bonusLists': [], 'buyout': 20000, 'quantity': 2},
            {'item': 1, 'bonusLists': [{'bonusListId': 1}], 'buyout': 20000, 'quantity': 2},
            {'item': 1, 'bonusLists': [{'bonusListId': 2}], 'buyout': 20000, 'quantity': 2},
            {'item': 2, 'bonusLists': [{'bonusListId': 3}, {'bonusListId': 4},], 'buyout': 20000, 'quantity': 1},
            {'item': 2, 'bonusLists': [{'bonusListId': 3}, {'bonusListId': 4},], 'buyout': 20000, 'quantity': 1}
        ]
        assert {(1,): {1: 2}, (1, 1): {1: 2}, (1, 2): {1: 2}, (2, 3, 4): {2: 2}} == parse_auctions(test2)