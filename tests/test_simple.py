from sampleproj.add_func import AddFunc


class TestAddFunc:
    def test_add_one(self):
        instance = AddFunc(1, 2)
        assert instance.add() == 3

    def test_add_two(self):
        instance = AddFunc(1, 3)
        assert instance.add() == 4
