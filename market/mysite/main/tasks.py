# mysite/tasks.py

# Celery에서 사용되는 비동기 작업 함수
from celery import shared_task
from .models import Commercial_data
from .serializers import commercial_dataSerializer, store_dataSerializer, Revenue_dataSerializer, population_dataSerializer, apart_dataSerializer

@shared_task
def process_uploaded_file(file_data, country, city):
    """
    업로드된 파일 데이터를 처리하는 Celery 작업 함수.
    
    Parameters:
    - file_data (dict): 업로드된 파일 데이터를 담은 딕셔너리.
    - country (str): 클라이언트에서 제출한 나라 정보.
    - city (str): 클라이언트에서 제출한 도시 정보.
    """
    # 파일 데이터를 반복하여 처리
    for i, value in file_data.items():
        # 만약 파일 이름에 'commercial_district'이 포함되어 있다면
        if "commercial_district" in i:
            # 상세한 처리를 commercial_district_uploaded_file 함수에 위임
            commercial_district_uploaded_file(value, country, city)
        else:
            # 그 외의 파일은 공통적인 처리 수행
            readLine = value
            header = readLine[0].split(',')
            datas = []

            # 각 라인의 데이터를 딕셔너리로 변환하여 리스트에 저장
            for k in readLine[1:-1]:
                dict = {name: value for name, value in zip(header, k.split(','))}
                datas.append(dict)

            # 각 데이터 처리
            for data in datas:
                new_data = data.copy()
                # 필요한 경우 데이터 변환 또는 추가 작업 수행
                for key, value in data.items():
                    if key in ['nation', 'city', 'commercial_name', 'service_code', 'service_name']:
                        continue
                    else:
                        if not str(value).isdigit():
                            new_data[key] = 0
                        else:
                            new_data[key] = int(value)
                
                # Commercial_data 모델 객체 가져오기
                try:
                    commercial_instance = Commercial_data.objects.get(
                        nation=country,
                        city=city,
                        commercial_code=data["commercial_code"]
                    )
                except Commercial_data.DoesNotExist:
                    print("Commercial_data matching query does not exist:", data)
                    continue

                # Commercial_data와 연결하고, 각 데이터에 맞는 Serializer 선택
                new_data["commercial"] = commercial_instance.pk

                if "market" in i:
                    serializer = store_dataSerializer(data=new_data)
                elif "sales" in i:
                    serializer = Revenue_dataSerializer(data=new_data)
                elif "apart" in i:
                    serializer = apart_dataSerializer(data=new_data)
                elif "people" in i:
                    serializer = population_dataSerializer(data=new_data)
                
                # Serializer가 유효하다면 저장, 그렇지 않으면 에러 출력
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)


@shared_task
def commercial_district_uploaded_file(readLine, country, city):
    """
    'commercial_district' 파일 데이터를 처리하는 Celery 작업 함수.
    
    Parameters:
    - readLine (list): 'commercial_district' 파일 데이터를 담은 리스트.
    - country (str): 클라이언트에서 제출한 나라 정보.
    - city (str): 클라이언트에서 제출한 도시 정보.
    """
    # 'commercial_district' 파일에 대한 처리
    header = readLine[0].split(',')
    datas = []

    # 각 라인의 데이터를 딕셔너리로 변환하여 리스트에 저장
    for k in readLine[1:-1]:
        dict = {name: value for name, value in zip(header, k.split(','))}
        datas.append(dict)

    # 각 데이터 처리
    for data in datas:
        new_data = data.copy()
        # 나라와 도시 정보 추가 및 필요한 경우 데이터 변환 작업 수행
        new_data["nation"] = country
        new_data["city"] = city
        
        # 만약 데이터의 'x' 키에 해당하는 값이 숫자가 아니면 0으로 대체하고, 숫자라면 그대로 사용
        if not str(new_data["x"]).isdigit():
            new_data['x'] = 0
        else:
            new_data['x'] = int(new_data['x'])
        # 만약 데이터의 'y' 키에 해당하는 값이 숫자가 아니면 0으로 대체하고, 숫자라면 그대로 사용
        if not str(new_data["y"]).isdigit():
            new_data['y'] = 0
        else:
            new_data['y'] = int(new_data['y'])
        
        # commercial_dataSerializer를 사용하여 데이터 저장
        serializer = commercial_dataSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            print(data)
