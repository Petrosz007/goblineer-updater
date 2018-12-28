import pytest, sys
sys.path.insert(0, '')
from src.marketvalue import marketvalue, dict_to_list, list_to_dict

class TestListToDict(object):
    # TODO: Type checking
    def test_correct_values(self):
        test0 = []
        assert {} == list_to_dict(test0)

        test1 = [1, 2,2, 3,3,3, 4,4,4,4, 5,5,5,5,5]
        assert {1: 1, 2: 2, 3: 3, 4: 4, 5: 5} == list_to_dict(test1)

        test2 = [6, 5,5, 6, 5,5, 6]
        assert {6: 3, 5: 4} == list_to_dict(test2)

class TestDictToList(object):
    # TODO: Type checking
    def test_correct_values(self):
        test0 = {}
        assert [] == dict_to_list(test0)

        test1 = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}
        assert [1, 2,2, 3,3,3, 4,4,4,4, 5,5,5,5,5] == dict_to_list(test1)

        test2 = {6: 3, 5: 4}
        assert [6,6,6, 5,5,5,5] == dict_to_list(test2)

class TestMarketvalue(object):
    def test_incorrect_types(self):
        with pytest.raises(TypeError):
            marketvalue([1,2,3])

    def test_correct_values(self):
        test0 = {}
        assert {'marketvalue': 0, 'quantity': 0, 'MIN': 0} == marketvalue(test0)

        test1 = {100: 2000}
        assert {'marketvalue': 100, 'quantity': 2000, 'MIN': 100} == marketvalue(test1)

        test2_raw = [5, 13, 13, 15, 15, 15, 16, 17, 17, 19, 20, 20, 20, 20, 20, 20, 21, 21, 29, 45, 45, 46, 47, 100]
        test2 = list_to_dict(test2_raw)
        print(test2)
        assert {'marketvalue': 14.5, 'quantity': 24, 'MIN': 5} == marketvalue(test2)

        test3 = {129.4372: 2, 57.1476: 1, 129.4373: 1}
        assert {'marketvalue': 57.1476, 'quantity': 24, 'MIN': 57.1476} == marketvalue(test3)

