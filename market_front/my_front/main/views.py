from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import logging
logger = logging.getLogger(__name__)


def data_upload(request):
    return render(request, 'data_upload.html')

def data_result(request):
    return render(request, 'data_result.html')

def data_process(request):
    return render(request, 'data_process.html')

def main(request):
    return render(request, 'map.html')
    
def get_trdar_cd(request):
    if request.method == 'GET':
        #trdar_cd_n: 상권 이름
        #trdar_cd: 상권 코드
        trdar_cd_n = request.GET.get('trdar_cd_n')
        trdar_cd = request.GET.get('trdar_cd')

        # 데이터를 요청할 URL
        url = "http://220.69.209.126:8880/api/get_trdar_cd"

        # GET 요청으로 데이터를 전송합니다.
        response = requests.get(url, params={'trdar_cd_n': trdar_cd_n, 'trdar_cd': trdar_cd})

        # 상태 코드 확인
        if response.status_code == 200:
            # JSON 데이터 추출
            data = response.json()

            # 나머지 데이터에 대한 처리
            commercial_data = data.get('commercial_data', {})
            store_data = data.get('store_data', 0)
            revenue_data = data.get('revenue_data', [])
            apart_data = data.get('apart_data', [])
            population_data = data.get('population_data', [])

            # 데이터 활용
            print(f'Commercial Data: {commercial_data}')
            print(f'Store Data: {store_data}')
            print(f'Revenue Data: {revenue_data}')
            print(f'Apart Data: {apart_data}')
            print(f'Population Data: {population_data}')

            return render(request, 'map.html',{'commercial_data':'commercial_data', 'store_data':store_data, 'revenue_data': revenue_data,'apart_data':apart_data,'population_data':population_data})
        else:
            print(f'요청이 실패하였습니다. 상태 코드: {response.status_code}')

    return render(request, 'map.html')

@csrf_exempt
def upload_file(request):
    file_name=["commercial_district", "market", "sales", "income_consumption", "commercial district_change", "apart", "people"]
    if request.method=="POST":
        files=request.FILES.getlist('file[]')
        # 파이썬 딕셔너리 형식으로 file 설정
        data = {}
        upload_name=""
        i=0
        for file in files:
            print(file)
            if file!="":
                data[str(file).split(".")[0]]=file
                upload_name=upload_name+str(file).split(".")[0]+","
                i+=1

        url="http://220.69.209.126:8880/api/upload_file"
        # print(upload_name)
        # print(upload)
        response=requests.post(url=url, files = data, data={"name":upload_name, "country":request.POST["country"], "city":request.POST["city"] })

    return redirect("main")
