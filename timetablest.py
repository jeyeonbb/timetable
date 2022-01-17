#timetable start.py를 노린 이름~


#untracked 뜨는 건 git에 업로드를 안 해서인가?

import json
import re
import pprint

#sample_json JSON 구문 분석 및 방출. 에는 JSON을 구문 분석하고 내보내는 방법이 나와 있습니다.
#음... json 예제 같은 건가 보다 -> 탐토님이 급식 예제로 만드신거니까 이걸 시간표 예제로!! 내가 바꾸기.

#!!sample_json{~~~} ~~~를 시간표관련된걸로 수정수정.. 으아아아ㅏ아 나이스 보면서 다시 유알엘 만들어야겠네.. 

sample_json = """{"hisTimetable":[{"head":[{"list_total_count":6},{"RESULT":{"CODE":"INFO-000","MESSAGE":"정상 처리되었습니다."}}]},{"row":[{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","AY":"2021","SEM":"2","ALL_TI_YMD":"20211224","DGHT_CRSE_SC_NM":"주간","ORD_SC_NM":"일반계","DDDEP_NM":"7차일반","GRADE":"2","CLRM_NM":"8","CLASS_NM":"8","PERIO":"1","ITRT_CNTNT":"자율활동","LOAD_DTM":"20211226"},{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","AY":"2021","SEM":"2","ALL_TI_YMD":"20211224","DGHT_CRSE_SC_NM":"주간","ORD_SC_NM":"일반계","DDDEP_NM":"7차일반","GRADE":"2","CLRM_NM":"8","CLASS_NM":"8","PERIO":"2","ITRT_CNTNT":"자율활동","LOAD_DTM":"20211226"},{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","AY":"2021","SEM":"2","ALL_TI_YMD":"20211224","DGHT_CRSE_SC_NM":"주간","ORD_SC_NM":"일반계","DDDEP_NM":"7차일반","GRADE":"2","CLRM_NM":"8","CLASS_NM":"8","PERIO":"3","ITRT_CNTNT":"자율활동","LOAD_DTM":"20211226"},{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","AY":"2021","SEM":"2","ALL_TI_YMD":"20211224","DGHT_CRSE_SC_NM":"주간","ORD_SC_NM":"일반계","DDDEP_NM":"7차일반","GRADE":"2","CLRM_NM":"8","CLASS_NM":"8","PERIO":"4","ITRT_CNTNT":"자율활동","LOAD_DTM":"20211226"},{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","AY":"2021","SEM":"2","ALL_TI_YMD":"20211224","DGHT_CRSE_SC_NM":"주간","ORD_SC_NM":"일반계","DDDEP_NM":"7차일반","GRADE":"2","CLRM_NM":"8","CLASS_NM":"8","PERIO":"5","ITRT_CNTNT":"진로활동","LOAD_DTM":"20211226"},{"ATPT_OFCDC_SC_CODE":"I10","ATPT_OFCDC_SC_NM":"세종특별자치시교육청","SD_SCHUL_CODE":"9300180","SCHUL_NM":"종촌고등학교","AY":"2021","SEM":"2","ALL_TI_YMD":"20211224","DGHT_CRSE_SC_NM":"주간","ORD_SC_NM":"일반계","DDDEP_NM":"7차일반","GRADE":"2","CLRM_NM":"8","CLASS_NM":"8","PERIO":"6","ITRT_CNTNT":"진로활동","LOAD_DTM":"20211226"}]}]}"""

sample_raw_data = json.loads(sample_json)
#json.load->json.dump를 역직렬화! 
#
pp = pprint.PrettyPrinter(indent=2)
#indent: 들여쓰기?

data = sample_raw_data["hisTimetable"][1]["row"][0]
#mealServiceDietINfo를 대체해야함! row는 냅둬도 되겠지.
#!! mealServiceDietINfo->

pp.pprint({
    "교시": int(data["PERIO"]),
    "날짜": data["ALL_TI_YMD"],
    "강의실명": data["CLRM_NM"],
    "학년": int(data["GRADE"]),
    "수업내용": data["ITRT_CNTNT"],
})
# re.sub:
#.split:
#시도교육청코드시도교육청명: I10(입력필수) 표준학교코드학교명: 9300180 *학년도 *학기 시간표일자 주야과정명:주간 계열명: 일반계 학과명: 7차일반 *학년 *강의실명 *반명 *교시 *수업내용 수정일
# 학년, 강의실명, 반명, 교시, 수업내용 -> 날짜도 있어야하는 거 아닌가?
#  :  강의실이랑 반명이 다른 경우는 이동수업인가보네 