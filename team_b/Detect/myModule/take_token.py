import requests
import json

url = 'https://kauth.kakao.com/oauth/token'
rest_api_key = '4b2e711c8d24870d3c840e51272b82ab'
redirect_uri = 'https://localhost.com'
authorize_code = 'Nr2FdZQGE26zEsa0QOMX3mNwrNeH5gQFh88pUk68PAASIKqeM2_fUt15mkJ5ejvd1xnFUAo9dGgAAAGAvBZY0w'

data = {
    'grant_type':'authorization_code',
    'client_id':rest_api_key,
    'redirect_uri':redirect_uri,
    'code': authorize_code,
    }

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)

with open("kakao_token/kakao_origin.json","w") as fp:
    json.dump(tokens, fp)
