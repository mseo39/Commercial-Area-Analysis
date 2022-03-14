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
#[1]
import pandas as pd

#상주인구
resident_population=pd.read_csv("서울시 우리마을가게 상권분석서비스(상권_상주인구).csv",encoding = 'cp949')
#생활인구
living_population=pd.read_csv("서울시 우리마을가게 상권분석서비스(상권-생활인구).csv",encoding = 'cp949')

#가장 최근 데이터만 가져온다(2021년 3분기가 가장 최근 데이터)
resident_population=resident_population[(resident_population["기준_년_코드"]==2021) & (resident_population["기준_분기_코드"]==3)]
living_population=living_population[(living_population["기준 년코드"]==2021) & (living_population["기준_분기_코드"]==3)]

resident_population

#[2]
living_population

#[4]
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
    data_list.append((living_population[living_population["상권_코드"]==i]["총_생활인구_수"].values- temp)[0])
living_population["생활인구-상주인구"]=data_list


#[5]
# 생활인구-상주인구 기준으로 내림차순 정렬

#ascending=False 내림차순으로 정렬하기 위해 사용
df_sorted_by_values = living_population.sort_values(by="생활인구-상주인구" ,ascending=False)
df_sorted_by_values

#[6]
from pyproj import Transformer

commercial_district=pd.read_csv("서울시 우리마을가게 상권분석서비스(상권영역).csv",encoding = 'cp949')
#위도는 y좌표 경도는 x좌표


# EPSG:5181을 EPSG:4326(위경도)로 변환하기

x_list=[]
y_list=[]
for i,row in commercial_district.iterrows():
    TRAN_4326_TO_3857 = Transformer.from_crs("EPSG:5181", "EPSG:4326")
    x, y = TRAN_4326_TO_3857.transform(row["엑스좌표_값"],row["와이좌표_값"] ) # 변환하는 과정
    x_list.append(x)
    y_list.append(y)
    
commercial_district["위도"]=y_list
commercial_district["경도"]=x_list
commercial_district


#[7]
"""
위 데이터로 지도에 표시했었는데 시각적으로 보기 불편하여
시군구로 나눈 다음에 클릭한 지역을 상권코드별로 시각적으로 보여준다

commercial_district에서 시군구 코드가 같은 열을 가져오고
그 열에서 상권코드를 찾고
living_population에서 이 상권코드를 가진 열을 찾은 다음에 생활인구-상주인구 값들을 전부 더해서
해당하는 리스트에 삽입해준다

"""

# 서울특별시 시군구 코드 리스트 생성
city_code=[['강남구', 11680], ['강동구', 11740], ['강북구', 11305], ['강서구', 11500], ['관악구', 11620], ['광진구', 11215], ['구로구', 11530], ['금천구', 11545], ['노원구', 11350], ['도봉구', 11320], ['동대문구', 11230], ['동작구', 11590], ['마포구', 11440], ['서대문구', 11410], ['서초구', 11650], ['성동구', 11200], ['성북구', 11290], ['송파구', 11710], ['양천구', 11470], ['영등포구', 11560], ['용산구', 11170], ['은평구', 11380], ['종로구', 11110], ['중구', 11140], ['중랑구', 11260]]

for i in city_code:
    temp=0
    for index,s in commercial_district[commercial_district["시군구_코드"]==i[1]].iterrows():
        if(living_population[living_population["상권_코드"]==s["상권_코드"]].empty==0):
            temp+= living_population[living_population["상권_코드"]==s["상권_코드"]]["생활인구-상주인구"].values[0]
    i.append(temp)

for i in city_code:
    print(i[0],i[1],i[2])
