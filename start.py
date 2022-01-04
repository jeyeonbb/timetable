import json
import re
import pprint

sample_json = """{"mealServiceDietInfo":[{"head":[{"list_total_count":1},{"RESULT":{"CODE":"INFO-000","MESSAGE":"정상 처리되었습니다."}}]},{"row":[{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","MMEAL_SC_CODE":"2","MMEAL_SC_NM":"중식","MLSV_YMD":"20211224","MLSV_FGR":"617","DDISH_NM":"미트볼 스파게티1.2.5.6.10.12.13.
페스츄리스프1.2.5.6.15.
아보카도샐러드&랜치드레싱(종촌1.2.5.6.10.11.12.13.치즈등갈비5.6.10.12.13.
오이피클9.13.
초코케이크(종촌)1.2.6.","ORPLC_INFO":"쌀 : 국내산
김치류 : 국내산
고춧가루(김치류) : 국내산
쇠고기(종류) : 국내산(한우)
돼지고기 : 국내산
닭고기 : 국내산
오리고기 : 국내산
쇠고기 식육가공품 : 국내산
돼지고기 식육가공품 : 국내산
닭고기 식육가공품 : 국내산
오리고기 가공품 : 국내산
낙지 : 국내산
고등어 : 국내산
갈치 : 국내산
오징어 : 국내산
꽃게 : 국내산
참조기 : 국내산
콩 : 국내산","CAL_INFO":"1305.3 Kcal","NTR_INFO":"탄수화물(g) : 144.2
단백질(g) : 42.1
지방(g) : 65.3
비타민A(R.E) : 367.3
티아민(mg) : 0.8
리보플라빈(mg) : 1.5
비타민C(mg) : 26.4
칼슘(mg) : 169.3
철분(mg) : 5.7","MLSV_FROM_YMD":"20211224","MLSV_TO_YMD":"20211224"}]}]}""".replace("\n", "\\n")

sample_raw_data = json.loads(sample_json)

pp = pprint.PrettyPrinter(indent=2)

data = sample_raw_data["mealServiceDietInfo"][1]["row"][0]
pp.pprint({
    "날짜": data["MLSV_YMD"],
    "시간": data["MMEAL_SC_NM"],
    "메뉴": re.sub('[\.0-9]', '', data["DDISH_NM"]).split("\n"),
})

# https://greeksharifa.github.io/%EC%A0%95%EA%B7%9C%ED%91%9C%ED%98%84%EC%8B%9D(re)/2018/08/04/regex-usage-05-intermediate/#%EC%A0%95%EA%B7%9C%EC%8B%9D-%EC%9D%BC%EC%B9%98%EB%B6%80%EB%A5%BC-%EB%AC%B8%EC%9E%90%EC%97%B4%EC%97%90%EC%84%9C-%EC%A0%9C%EA%B1%B0