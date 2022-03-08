'''
1. 어느지역에 유동인구가 많은지 데이터 정리
2. 유동인구 데이터 시각적으로 표현 (유동인구가 많을수록 진한색)
3. 각 지역의 매출이 높은 업종 정리 (3개 정도)
4. 관련된 가게들 위치 표시 

사용한 데이터
서울시 우리마을가게 상권분석서비스(상권_상주인구)
서울시 우리마을가게 상권분석서비스(상권-생활인구)
서울시 우리마을가게 상권분석서비스(상권영역) *평면좌표계(EPSG 5181)로 작성됨
서울시 우리마을가게 상권분석서비스(상권-추정매출)

상주인구는 "서울시 주민등록주소 기반으로 작성한 인구수"
생활인구는 "서울시와 KT가 공공빅데이터와 통신데이터를 이용하여 작성한 서울의 특정지역, 특정시점에 존재하는 인구수"

사람들이 모이는 지역을 알고싶기 때문에 생활인구-상주인구를 구했다
상주인구가 많아서 생활인구가 많이 집계되는 것일 수 있기 때문
'''

import pandas as pd

#상주인구
resident_population=pd.read_csv("서울시 우리마을가게 상권분석서비스(상권_상주인구).csv",encoding = 'cp949')
#생활인구
living_population=pd.read_csv("서울시 우리마을가게 상권분석서비스(상권-생활인구).csv",encoding = 'cp949')

#가장 최근 데이터만 가져온다(2021년 3분기가 가장 최근 데이터)
resident_population=resident_population[(resident_population["기준_년_코드"]==2021) & (resident_population["기준_분기_코드"]==3)]
living_population=living_population[(living_population["기준 년코드"]==2021) & (living_population["기준_분기_코드"]==3)]

resident_population

living_population

#생활인구-상주인구 값을 저장할 빈 리스트 생성
data_list=[]

#생활인구-상주인구
for i in living_population["상권_코드"]:
    # 생활인구데이터에 없는 상권 코드라면
    if resident_population[resident_population["상권 코드"]==i]["총 상주인구 수"].empty:
        #0으로 설정
        temp=0
    else:
        #상주인구 데이터를 가져옴
        temp=resident_population[resident_population["상권 코드"]==i]["총 상주인구 수"].values
    data_list.append(living_population[living_population["상권_코드"]==i]["총_생활인구_수"].values- temp)
   

# 생활인구-상주인구 기준으로 내림차순 정렬

#ascending=False 내림차순으로 정렬하기 위해 사용
df_sorted_by_values = living_population.sort_values(by="생활인구-상주인구" ,ascending=False)
df_sorted_by_values