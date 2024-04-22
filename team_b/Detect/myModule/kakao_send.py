import json
import requests
import datetime
import os
import time

class Kakao:
    def __init__(self):
        self.KAKAO_TOKEN = "myModule/kakao_token/kakao_access.json"
        self.KAKAO_Ori = "myModule/kakao_token/kakao_origin.json"
        self.KAKAO_APP_KEY = "4b2e711c8d24870d3c840e51272b82ab"

    def save_tokens(self, filename, tokens):#Token키를 저장함
        with open(filename, "w") as fp:
            json.dump(tokens, fp)

    def load_tokens(self, filename):#Token키를 불러옴
        with open(filename, "r") as fp:
            tokens = json.load(fp)
        return tokens

    def update_tokens(self):
        now = time.time()#만료기간 판별을 위해 현재시간을 구함
        tokens_make = os.path.getmtime(self.KAKAO_TOKEN)#토큰의 생성 시간을 구함
        tokens = self.load_tokens(self.KAKAO_TOKEN)#kakao_access토큰을 불러옴

        if 'error' in list(tokens.keys()) or now-tokens_make > tokens['expires_in']:
        #access토큰을 다시 받아야 되는 경우를 표현
            print('token을 새로 받습니다')
            kakao_ori = self.load_tokens(self.KAKAO_Ori)
            url = "https://kauth.kakao.com/oauth/token"
            
            #data 꾸리기
            data = {
                "grant_type" : "refresh_token",
                "client_id" : self.KAKAO_APP_KEY,
                "refresh_token" : kakao_ori['refresh_token']
            }

            #access키 받기
            response = requests.post(url, data=data)
            tokens = response.json()
            if 'error' in list(tokens.keys()):
                print('OriginKey 만료되었습니다. 교체 필요!')
                return 0

        if 'refresh_token' in tokens:   self.save_tokens(self.KAKAO_Ori, tokens)
        else:   self.save_tokens(self.KAKAO_TOKEN, tokens)
        #갱신 토큰 저장

        return tokens

    def send_message(self, detect_num, temperature):#온도 이상자만 메시지 보냄

        token = self.update_tokens()

        url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        if detect_num == '-':   detect_num = '미등록'
        text = f"연락처: {detect_num}의 사람이 {str(temperature)}°C 로 출입 정지!"

        header = {
            "Authorization" : "Bearer " + token["access_token"]
        }

        post = {
            "object_type" : "text",
            "text" : text,
            "link" : {
                "web_url" : "https://developers.kakao.com",
                "mobile_web_url" : "https://developers.kakao.com"
            },
            "botton_title" : "체온이상 감지!"
        }

        data = {"template_object" : json.dumps(post)}

        if temperature > 37.5:
            requests.post(url, headers=header, data=data)

if __name__=="__main__":
    a = Kakao()
    a.send_message(1, 39.5)
