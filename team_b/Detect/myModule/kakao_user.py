import requests
import json
import os

def receive_info():

    url = "https://kapi.kakao.com/v2/user/me"
    header = {
        "Authorization" : "Bearer " + "23x4ZoovyvX-b2Ch8zBRaPrfIq8Wx9JqWLX2_go9c00AAAGAvBjo7w"
    }
    profile_request = requests.get(url, headers=header)
    tokens = profile_request.json()
    print(tokens)

if __name__=="__main__":    receive_info()
