from urllib.parse import urlencode, unquote
import requests
import json



ls_url = "http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
ls_url2 = "?" + urlencode(

        {

                "ServiceKey" : unquote("G4BAlqMRQ8zvwk%2B6cWOcAcpqw1iKNkD71Ch4jWfLX6gxhCBdSkaae2NVGg6VumH1ojcRVsgDrJF3Mm5cfU76cQ%3D%3D"),

                "base_date" : "20220415",

                "base_time" : "1700",

                "nx" : "57",

                "ny" : "121",

                "numOfRows" : "1000",

                "pageNo" : "1",

                "dataType" : "JSON",

        }

)

ls_queryurl = ls_url + ls_url2

response = requests.get(ls_queryurl) #해당url주소의 데이터를 가져와서 response에 담는다

ls_dict = json.loads(response.text) #json문자열을 파이썬 객체로 변환한다.
ls_response = ls_dict.get("response")

ls_body = ls_response.get("body")

ls_items = ls_body.get("items")

ls_item = ls_items.get("item")


result={} # result라는 딕셔너리 변수를 선언함, 딕셔너리는 초기화를 해야 사용할수 있다
result_dict={}  # result_dict라는 키와 값을 담아둘 딕셔너리를 선언하고 초기화를 시킨다.


#루프문에서 result_dict 에는 키와 값을 담아둔다 예)result_dict['PTY']='0'  , result_status['REH']='97'
for item in ls_item:  #ls_item에 들어있는 배열의 개수만큼 반복함

    result=item

    print(result)

    result_dict.setdefault(result.get("category"),result.get("obsrValue"))


print("날짜 : "+result.get("baseDate")[:-4]+"년"+result.get("baseDate")[4:-2]+"월"+result.get("baseDate")[6:]+"일"+"시간 : " + result.get("baseTime")[:-2]+"시")
print("강우형태 : "+result_dict["PTY"])
print("습도 : "+result_dict["REH"]+" %")
print("1시간 강수량 : " +result_dict["RN1"]+" mm")
print("기온 : "+result_dict["T1H"] +" ℃")
print("동서바람성분 : " +result_dict["UUU"]+" m/s")
print("남북바람성분 : " + result_dict["VVV"]+" m/s")
print("풍향 : "+result_dict["VEC"])
print("풍속 : "+result_dict["WSD"])