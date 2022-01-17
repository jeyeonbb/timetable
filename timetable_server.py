#time table server..! 를 의미하는 이름~

from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from requests import HTTPError
import pprint
import json
import re
import os 

app = FastAPI() #앱. 핵심!
# python -m uvicorn server:app --port 8000

@app.get("/")
def root():
    return '<a href="./docs">API 문서 보기</a>'


class TimeTable(BaseModel):
    교시: int
    날짜: str
    강의실명: str
    학년: int
    수업내용: str
#!!!!start에서 했던대로 수정하기러기 -> 학년, 강의실명, 반명, 교시, 수업내용


#30~70..!! 여기가 난관이다!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! meal_ymd 를 대체...! 음 timetable_ymd?
@app.get("/timetable/{grade}/{class_number}/{timetable_ymd}", response_model=List[TimeTable])
def meal(grade: int, class_number: int, timetable_ymd: str):

    # 학년, 반에 해당하는 폴더가 없으면
    base_path = f"./data/{grade}/{class_number}" #폴더 위치
    if not os.path.exists(base_path):
        # 폴더들을 생성한다... "파이썬에서 재귀적으로 디렉터리 만들기"
        os.makedirs(base_path, exist_ok=True)


    # 데이터 폴더에 날짜에 해당하는 json 백업 파일이 있으면...
    file_path = base_path + f"/{timetable_ymd}.json" # 파일 위치
    if os.path.exists(file_path): # 파이썬 파일 존재 여부
        # 그 파일을 (읽기 모드 r->파이썬 존재여부에서 본거같다) 로 열고
        with open(file_path, "r", encoding="UTF-8") as f:
            # 파일 내용을 읽어요
            raw_json = f.read() #파일이 잇으면 읽어오기
            # json 텍스트 파일을 파이썬 딕셔너리로 변환 (역직렬화)
            raw_data = json.loads(raw_json)
            print(f"백업해둔 {base_path}/{timetable_ymd} 데이터를 불러왔습니다.")
    else:
        # 급식 api의 url에 날짜만 query string으로 바꿔서
        url = f"https://open.neis.go.kr/hub/hisTimetable?KEY=bd6cfbba1e2c46768398d040d90c2a33&Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=I10&SD_SCHUL_CODE=9300180&ALL_TI_YMD={timetable_ymd}&CLASS_NM={class_number}&GRADE={grade}"
        
        # 요청해서 서버에서 응답, 즉 response가 돌아오면
        response = requests.get(url)
        # 응답에서 json을 해석해서 파이썬 딕셔너리로 꺼낸다
        raw_data = response.json() #없으면 url

        #파이썬 파일처리 구글검색
        # data폴더(종이 두 개 겹친거)에 {meal_ymd}.json라는 이름으로 w 쓰기 모드로 파일을 만들어서
        with open(file_path, "w", encoding="UTF-8") as f:
            # 파이썬 딕셔너리를 json 텍스트 파일로 변환 (직렬화. dumps)
            raw_json = json.dumps(raw_data, ensure_ascii=False)
            # 파일에 써준다
            f.write(raw_json) 
        print(f"서버에서 {timetable_ymd} 데이터를 불러왔습니다.")

    if "hisTimetable" not in raw_data:
        print(raw_data)
        # {'RESULT': {'CODE': 'INFO-200', 'MESSAGE': '해당하는 데이터가 없습니다.'}}
        if raw_data['RESULT']['MESSAGE'] == '해당하는 데이터가 없습니다.':
            raise HTTPException(
                status_code=404,
                detail="수업이 없는 날입니다"
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
    data_list = raw_data["hisTimetable"][1]["row"]


    # 날짜 시간 메뉴를 정리해서 프런트엔드에게 보내준다!!
    # 파이썬의 리스트 컴프리헨션
    return [{
        "교시": int(data["PERIO"]),
        "날짜": data["ALL_TI_YMD"],
        "강의실명": data["CLRM_NM"],
        "학년": int(data["GRADE"]),
        "수업내용": data["ITRT_CNTNT"],
    } for data in data_list]


# http://localhost:8000/docs
# python -m uvicorn server:app -> 서버 키는 법 
# 해석 : 파이썬아, module인, uvicorn으로, server파일의, app을 실행해

# python -m uvicorn server:app --reload

