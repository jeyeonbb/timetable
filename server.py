from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from requests import HTTPError
import pprint
import json
import re
import os #파이썬 파일 존재 여부

app = FastAPI() #앱. 핵심!
# python -m uvicorn server:app --port 8000
# 파이썬 친구야. 모듈인 uvicorn 을 가지고 server 파일에 있는 app을 실행시켜줘!!
# ip 포트포워딩...! 다른컴퓨터에서 들어올 수 있게 ~

@app.get("/")
def root():
    return '<a href="./docs">API 문서 보기</a>'

class Meal(BaseModel):
    날짜: str
    시간: str
    메뉴: List[str]

# 20211223
# yyyymmdd
@app.get("/meal/{meal_ymd}", response_model=Meal)
def meal(meal_ymd: str):
    # 데이터 폴더에 날짜에 해당하는 json 백업 파일이 있으면...
    if os.path.exists(f"./data/{meal_ymd}.json"): # 파이썬 파일 존재 여부
        # 그 파일을 (읽기 모드 r->파이썬 존재여부에서 본거같다) 로 열고
        with open(f"./data/{meal_ymd}.json", "r", encoding="UTF-8") as f:
            # 파일 내용을 읽어요
            raw_json = f.read() #파일이 잇으면 읽어오기
            # json 텍스트 파일을 파이썬 딕셔너리로 변환 (역직렬화)
            raw_data = json.loads(raw_json)
            print(f"백업해둔 {meal_ymd} 데이터를 불러왔습니다.")
    else:
        # 급식 api의 url에 날짜만 query string으로 바꿔서
        url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY=bd6cfbba1e2c46768398d040d90c2a33&Type=json&ATPT_OFCDC_SC_CODE=I10&SD_SCHUL_CODE=9300180&MLSV_YMD={meal_ymd}"
        
        # 요청해서 서버에서 응답, 즉 response가 돌아오면
        response = requests.get(url)
        # 응답에서 json을 해석해서 파이썬 딕셔너리로 꺼낸다
        raw_data = response.json() #없으면 url

        #파이썬 파일처리 구글검색
        # data폴더(종이 두 개 겹친거)에 {meal_ymd}.json라는 이름으로 w 쓰기 모드로 파일을 만들어서
        with open(f"./data/{meal_ymd}.json", "w", encoding="UTF-8") as f:
            # 파이썬 딕셔너리를 json 텍스트 파일로 변환 (직렬화. dumps)
            raw_json = json.dumps(raw_data, ensure_ascii=False)
            # 파일에 써준다
            f.write(raw_json) 
        print(f"서버에서 {meal_ymd} 데이터를 불러왔습니다.")

    if "mealServiceDietInfo" not in raw_data:
        print(raw_data)
        # {'RESULT': {'CODE': 'INFO-200', 'MESSAGE': '해당하는 데이터가 없습니다.'}}
        if raw_data['RESULT']['MESSAGE'] == '해당하는 데이터가 없습니다.':
            raise HTTPException(
                status_code=404,
                detail="급식이 없는 날입니다"
            )
        raise HTTPException(
            status_code=response.status_code,
            detail=raw_data['RESULT']['MESSAGE']
        )

    # https://developer.mozilla.org/ko/docs/Web/HTTP/Status
    # 200 ok  => 잘 됐다! 데이터 잘 보내줄게!
    # 404 not found => 네가 요청한 데이터 못 찾았는데? 없는데?
    # 422 Unprocessable Entity => 내가 이거 처리하는데... 좀 이상해. 너 잘못 보낸 거 아냐?
    # 500 internal server error => 내가 하는데 문제가 생겼어...

    # 필요한 데이터만 꺼내서!
    data = raw_data["mealServiceDietInfo"][1]["row"][0]

    # 날짜 시간 메뉴를 정리해서 프런트엔드에게 보내준다!!
    return {
        "날짜": data["MLSV_YMD"], #str
        "시간": data["MMEAL_SC_NM"],
        "메뉴": re.sub('[\.0-9]', '', data["DDISH_NM"]).split("<br/>"), #List[str] #split 쪼개기 
        # "원산지": re.sub('[\.0-9]', '', data["ORPLC_INFO"]).split("<br/>"), #re.sub은 숫자 지우기

    }


# http://localhost:8000/docs
# python -m uvicorn server:app -> 서버 키는 법
# 해석 : 파이썬아, module인, uvicorn으로, server파일의, app을 실행해

# python -m uvicorn server:app --reload

# terminal에 입력하면 됌. 매번 켜줘야한다니 매우 번거롭다.

# fastapi ! 데이터는 json에 쌓이고 잇구~ 필요한건 얼마든지 추가 가능가능 
# os.re...! 안나온 기능도 연마하기.!!!!!!!!! 딕셔너리 슉슉슉 