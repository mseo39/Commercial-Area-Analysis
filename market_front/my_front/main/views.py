from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def main(request):
    return render(request, 'map.html')

def data_upload(request):

    return render(request, 'data_upload.html')

def data_result(request):
    return render(request, 'data_result.html')

def data_process(request):
    return render(request, 'data_process.html')


import logging
logger = logging.getLogger(__name__)
    
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
            count = data.get('total_store_num', 0)
            print(f'서버로부터 받은 count: {count}')
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
            
def upload(request):
    if request.method=='POST':
        file=request.FILES['file']
        
        # 파이썬 딕셔너리 형식으로 file 설정
        upload = {'file':file}

        # String 포맷
        obj={"temperature":'23.5', "humidity":'54.5'}

        url="http://127.0.0.1:8000/api/test"

        response=requests.post(url, files = upload, data = obj)

    return redirect("main")