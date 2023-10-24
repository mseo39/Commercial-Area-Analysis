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
    if request.method == 'POST':
        name = request.POST['name']
        country=request.POST["country"]
        city=request.POST["city"]
        logger.error(country)
        logger.error(city)

        file_data={}
        for i in name.split(","):
            if i!="":
                logger.error(i)
                uploadFile = request.FILES[i]
                read = uploadFile.read().decode('utf-8-sig')
                readLine = read.split('\r\n')
                file_data[i]=readLine

        process_uploaded_file.delay(file_data,country,city)

        return JsonResponse({'message': '파일 업로드 작업이 시작되었습니다.'}, status=status.HTTP_202_ACCEPTED)

    return JsonResponse({'message': 'Tutorials were deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

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