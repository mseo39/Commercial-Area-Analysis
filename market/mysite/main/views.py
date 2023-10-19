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
                'service_code','quarterly_sales', 'male_sales_ratio', 'female_sales_ratio'
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
                    'commercial_name': commercial_data.commercial_name,
                    'x': commercial_data.x,
                    'y': commercial_data.y,
                    'county_code': commercial_data.county_code,
                    'administrative_code': commercial_data.administrative_code,
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

"""def get_trdar_cd(request):
    if request.method == 'GET':
        trdar_cd_n = request.GET.get('trdar_cd_n')
        trdar_cd = request.GET.get('trdar_cd')

        # CS200001, CS200002, CS200003, CS200004 중 하나인 service_code를 가진 상점들을 필터링하고 store_num을 합산
        total_store_num = Store_data.objects.filter(
            commercial__commercial_code=trdar_cd,
            service_code__in=['CS200001', 'CS200002', 'CS200003', 'CS200004']
        ).aggregate(total_store_num=Sum('store_num'))['total_store_num']

        # 합산된 값을 반환
        return JsonResponse({'total_store_num': total_store_num}, status=status.HTTP_200_OK)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)
"""

"""@api_view(['POST'])
def test_data(request):
    return JsonResponse(status=status.HTTP_400_BAD_REQUEST)
    
    from rest_framework.response import Response
#
# @api_view(['GET'])
# def get_store_num(request):
#     admin_code = request.GET.get('admin_code', None)
#     # 주어진 administrative_code에 해당하는 Store_data를 가져옵니다.
#     store_data_list = Store_data.objects.filter(commercial__administrative_code=admin_code)
    
#     # (year, quarter)를 기준으로 store_num을 합산합니다.
#     store_num_sum_by_quarter = store_data_list.values('year', 'quarter').annotate(total_store_num=Sum('store_num'))
    
#     # quarter를 최신부터 나열하도록 정렬합니다.
#     store_num_sum_by_quarter = store_num_sum_by_quarter.order_by('-year', '-quarter')
    
#     # 최근 데이터 4개만 추출합니다.
#     recent_data = store_num_sum_by_quarter[:4]
#     recent_data_list = list(recent_data)
    
#     return Response(recent_data_list)

#점포의 개수를 구하는 함수
@api_view(['GET'])
def get_store_num(request):
    try:
        # GET 요청에서 administrative_code 가져오기
        administrative_code = request.GET.get('administrative_code', None)
        # administrative_code에 해당하는 commercial_code 가져오기
        commercial_code_list = Commercial_data.objects.filter(administrative_code=administrative_code).values_list('commercial_code', flat=True)
        # 해당 commercial_code를 가진 Store_data 가져오기
        store_data_list = Store_data.objects.filter(commercial__commercial_code__in=commercial_code_list)

        # (year, quarter)를 기준으로 store_num 합산하기
        store_num_sum_by_quarter = store_data_list.values('year', 'quarter').annotate(total_store_num=Sum('store_num'))

        store_num_sum_by_quarter = store_num_sum_by_quarter.order_by('-year', '-quarter')
        recent_data = store_num_sum_by_quarter[:min(4, len(store_num_sum_by_quarter))]

        
        # 결과를 (year, quarter, total_store_num) 형태로 정리
        result = [
            {'year': item['year'], 'quarter': item['quarter'], 'total_store_num': item['total_store_num']}
            for item in recent_data
        ]
        
        return JsonResponse(result, safe=False)  # JsonResponse로 결과 반환
    except Commercial_data.DoesNotExist:
        return JsonResponse({"error": "No Commercial data found for the given administrative code."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#프랜차이점의개수를 구하는 함수
@api_view(['GET'])
def get_franchisee_store_num_sum(request):
    try:
        # GET 요청에서 administrative_code 가져오기
        administrative_code = request.GET.get('administrative_code', None)
        # administrative_code에 해당하는 commercial_code 가져오기
        commercial_code_list = Commercial_data.objects.filter(administrative_code=administrative_code).values_list('commercial_code', flat=True)
        # 해당 commercial_code를 가진 Store_data 가져오기
        store_data_list = Store_data.objects.filter(commercial__commercial_code__in=commercial_code_list)

        # 해당 Commercial_data에 연결된 Store_data 중 가장 큰 year 값 가져오기
        max_year = store_data_list.aggregate(Max('year'))['year__max']
        print(max_year)

        if max_year is None:
            return 0

        # 해당 year 값에 대한 Store_data들 중 가장 큰 quarter 값을 가져오기
        max_quarter = store_data_list.aggregate(Max('quarter'))['quarter__max']
        print(max_quarter)
        if max_quarter is None:
            return 0

        # 해당 year와 quarter에 대한 Store_data들의 franchisee_store_num 합 구하기
        franchisee_store_num_sum = store_data_list.filter(
            year=max_year,
            quarter=max_quarter
        ).aggregate(Sum('franchisee_store_num'))['franchisee_store_num__sum']

        return JsonResponse({"num":franchisee_store_num_sum}, safe=False)  # JsonResponse로 결과 반환
    except Commercial_data.DoesNotExist:
        return JsonResponse({"error": "No Commercial data found for the given administrative code."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'POST', 'DELETE'])
def tutorial_list(request):
    if request.method == 'GET':
        tutorials = Tutorial.objects.all()
        
        title = request.GET.get('title', None)
        if title is not None:
            tutorials = tutorials.filter(title__icontains=title)
        
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)
        # 'safe=False' for objects serialization
 
    elif request.method == 'POST':
        tutorial_data = JSONParser().parse(request)
        print(type(request))
        print(type(tutorial_data)) #class 'dict'
        tutorial_serializer = TutorialSerializer(data=tutorial_data)
        if tutorial_serializer.is_valid():
            tutorial_serializer.save()
            return JsonResponse(tutorial_serializer.data, status=status.HTTP_201_CREATED) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        count = Tutorial.objects.all().delete()
        return JsonResponse({'message': '{} Tutorials were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(['GET', 'PUT', 'DELETE'])
def tutorial_detail(request, pk):
    try: 
        tutorial = Tutorial.objects.get(pk=pk) 
    except Tutorial.DoesNotExist: 
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET': 
        tutorial_serializer = TutorialSerializer(tutorial) 
        return JsonResponse(tutorial_serializer.data) 
 
    elif request.method == 'PUT': 
        tutorial_data = JSONParser().parse(request) 
        tutorial_serializer = TutorialSerializer(tutorial, data=tutorial_data) 
        if tutorial_serializer.is_valid(): 
            tutorial_serializer.save() 
            return JsonResponse(tutorial_serializer.data) 
        return JsonResponse(tutorial_serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
 
    elif request.method == 'DELETE': 
        tutorial.delete() 
        return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
    
        
@api_view(['GET'])
def tutorial_list_published(request):
    tutorials = Tutorial.objects.filter(published=True)
        
    if request.method == 'GET': 
        tutorials_serializer = TutorialSerializer(tutorials, many=True)
        return JsonResponse(tutorials_serializer.data, safe=False)"""