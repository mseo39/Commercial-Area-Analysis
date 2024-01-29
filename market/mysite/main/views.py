from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from main.serializers import *
from rest_framework.decorators import api_view
import json
from django.db.models import Sum, Max
from django.shortcuts import get_object_or_404


# myapp/views.py

from main.tasks import process_uploaded_file
import logging

logger = logging.getLogger(__name__)

#파일 업로드 기능
@api_view(['POST'])
def upload_file(request):
    # POST 메서드로 요청이 들어온 경우에만 처리
    if request.method == 'POST':
        # 클라이언트에서 전송한 데이터 가져오기
        name = request.POST['name']
        country = request.POST["country"]
        city = request.POST["city"]

        # 로그에 나라와 도시 정보 출력
        logger.error(country)
        logger.error(city)

        # 업로드된 파일들의 데이터를 저장할 딕셔너리 초기화
        file_data = {}
        # 전송된 파일들을 반복하여 처리
        for i in name.split(","):
            if i != "":
                logger.error(i)
                # 클라이언트에서 전송된 파일 중 하나를 선택하여 업로드된 파일 객체를 가져옴
                uploadFile = request.FILES[i]
                # 파일 내용을 UTF-8 형식으로 디코딩하면서 BOM(Byte Order Mark) 문자열 제거
                # BOM 문자열은 텍스트 파일의 처음에 위치하며, 파일이 어떤 인코딩 방식을 사용하는지 나타냄
                read = uploadFile.read().decode('utf-8-sig')
                # 읽어들인 파일 내용을 개행 문자('\r\n')를 기준으로 분리하여 리스트로 저장
                # Windows 환경에서의 개행 문자는 '\r\n'
                readLine = read.split('\r\n')
                # 파일 데이터 딕셔너리에 파일 이름(key)과 내용(value)을 저장
                file_data[i] = readLine

        # 비동기적으로 파일 처리 작업 시작
        process_uploaded_file.delay(file_data, country, city)

        # JsonResponse 메시지 수정 및 응답 상태코드 지정
        return JsonResponse({'message': '파일 업로드 작업이 시작되었습니다.', 'status': 'ACCEPTED'}, status=status.HTTP_202_ACCEPTED)

    # POST 요청이 아닌 경우에는 다른 응답을 반환
    return JsonResponse({'message': '올바르지 않은 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from main.models import Store_data, Revenue_data, Apart_data, Population_data, Commercial_data
from django.db.models import Sum

def get_commercial_data(request):
    if request.method == 'GET':
        trdar_cd = request.GET.get('trdar_cd')

        try:
            # 해당 trdar_cd에 해당하는 Commercial_data 레코드를 가져옵니다.
            commercial_data = Commercial_data.objects.get(commercial_code=trdar_cd)

            # Store_data: service_code가 'CS200001', 'CS200002', 'CS200003', 'CS200004'이면서 store_num 합산
            store_data = Store_data.objects.filter(
                commercial=commercial_data,
                service_code__in=['CS200001', 'CS200002', 'CS200003', 'CS200004']
            ).aggregate(total_store_num=Sum('store_num'))['total_store_num']

            # Revenue_data: commercial_code가 일치하면서 필요한 필드들을 가져옵니다.
            revenue_data = Revenue_data.objects.filter(commercial=commercial_data).values(
                'service_name','quarterly_sales', 'male_sales_ratio', 'female_sales_ratio'
            )

            # Apart_data: commercial_code가 일치하면서 모든 필드를 가져옵니다.
            apart_data = Apart_data.objects.filter(commercial=commercial_data).values(
                'apart_num','apart_1underprice','apart_1price','apart_2price','apart_3price','apart_4price','apart_5price','apart_6price'
            )

            # Population_data: commercial_code가 일치하면서 필요한 필드들을 가져옵니다.
            population_data = Population_data.objects.filter(commercial=commercial_data).values(
                'total_population', 'male_population', 'female_population', 'age10_population',
                'age20_population', 'age30_population', 'age40_population', 'age50_population', 'age60_population'
            )

            # JSON 형식으로 데이터를 구성
            response_data = {
                'commercial_data': {
                    'nation': commercial_data.nation,
                    'city': commercial_data.city,
                    'commercial_name': commercial_data.commercial_name
                },
                'store_data': store_data,
                'revenue_data': list(revenue_data),  # QuerySet을 리스트로 변환
                'apart_data': list(apart_data),  # QuerySet을 리스트로 변환
                'population_data': list(population_data),  # QuerySet을 리스트로 변환
            }

            return JsonResponse(response_data, status=200)
        except Commercial_data.DoesNotExist:
            return JsonResponse({'message': 'Commercial data not found.'}, status=404)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
