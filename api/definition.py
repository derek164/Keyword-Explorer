import requests
from requests.utils import requote_uri


def get_definition(term):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{term}"
    response = requests.get(requote_uri(url)).json()
    if isinstance(response, list):
        return [
            elem["definition"] for elem in response[0]["meanings"][0]["definitions"]
        ]
        # return response[0]["meanings"][0]["definitions"][0]["definition"]

if __name__ == "__main__":
    print(get_definition("queries"))
    print(get_definition("internet"))
    print(get_definition("semantics"))
    print(get_definition("processors"))
    print(get_definition("data mining"))
    print(get_definition("sensor networks"))
    print(get_definition("machine learning"))
    print(get_definition("programming language"))
    print(get_definition("approximation algorithms"))
    print(get_definition("natural language processing"))
