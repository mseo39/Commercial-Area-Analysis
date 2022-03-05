import pandas as pd

#필요한 데이터만 정리하는 함수
def data_export(file,serial):
    #파일 읽기
    data=pd.read_csv(file,encoding = 'cp949')
    #방문자수 데이터가 서버타입에 해당되어 읽혀짐
    
    dates=set()
    for i in data["방문자수"]:
        i=i.split(" ")
        dates.add(i[0])
    
    #날짜별로 나눈다(날짜가 키값)
    date_dict={}
    for date in dates:
        date_data=data[data["방문자수"]==date]
        serial_dict={}
        for i in serial:
            serial_temp=data[data['시리얼']==i]
            serial_dict[i]=(serial_temp["서버타입"].sum())
        date_dict[date]=serial_dict
    

#시리얼 종류가 담겨있는 파일
serial=pd.read_excel("(공개용)도시데이터센서(S-DoT) 유동인구정보 설치 위치정보_211125.xlsx", header=2)
    


#유동인구 파일 경로 리스트
file_name=["S-DoT_WALK_2021.12.27-01.02.csv",
           "S-DoT_WALK_2022.01.03-01.09.csv",
           "S-DoT_WALK_2022.01.10-01.16.csv",
           "S-DoT_WALK_2022.01.17-01.23.csv",
           "S-DoT_WALK_2022.01.31-02.06.csv",
           "S-DoT_WALK_2022.02.07-02.13.csv",
          ]

#각 시리얼별
floating_population=[]
for file in file_name:
    floating_population.append(data_export(file,serial["사이트명"]))

for i in floating_population:
    print(i)
    print("\n\n")
