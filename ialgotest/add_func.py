import requests


class AddFunc:
    def __init__(self, a, b):
        self._a = a
        self._b = b

    def add(self):
        return self._a + self._b

    def request_url(self):
        r = requests.get('http://www.baidu.com/')
        print(r.text)
