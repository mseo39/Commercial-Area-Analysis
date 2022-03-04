import pandas as pd

data=pd.read_csv("S-DoT_WALK_2022.01.31-02.06.csv",encoding = 'cp949')
data=data[["시리얼","서버타입"]]
data.columns = ["시리얼", "방문자수"]
data.set_index("시리얼",inplace=True)
print(data)

serial=pd.read_excel("(공개용)도시데이터센서(S-DoT) 유동인구정보 설치 위치정보_211125.xlsx", header=2)
serial_list=list(serial["사이트명"])
print(*serial_list)

