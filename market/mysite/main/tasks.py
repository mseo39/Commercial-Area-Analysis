# mysite/tasks.py

from celery import shared_task
from .models import Commercial_data
from .serializers import commercial_dataSerializer, store_dataSerializer,Revenue_dataSerializer, population_dataSerializer,apart_dataSerializer

@shared_task
def process_uploaded_file(file_data,country,city):
    for i, value in file_data.items() :
        
        if "commercial_district" in i:
            commercial_district_uploaded_file(value,country,city)
        else:
            readLine=value
            header = readLine[0].split(',')
            datas = []

            for k in readLine[1:-1]:
                dict = {name: value for name, value in zip(header, k.split(','))}
                datas.append(dict)

            for data in datas:
                new_data = data.copy()
                for key, value in data.items():
                    if key in ['nation','city','commercial_name','service_code','service_name']:
                        continue
                    else:
                        if str(value).isdigit()==False:
                            new_data[key]=0
                        else:
                            new_data[key]=int(value)
                try:
                    commercial_instance = Commercial_data.objects.get(
                    nation=country,
                    city=city,
                    commercial_code=data["commercial_code"]
                )
                except Commercial_data.DoesNotExist:
                    print("Commercial_data matching query does not exist:", data)
                    continue

                new_data["commercial"]=commercial_instance.pk

                if "market" in i:
                    serializer = store_dataSerializer(data=new_data)
                elif "sales" in i:
                    serializer = Revenue_dataSerializer(data=new_data)
                elif "apart" in i:
                    serializer = apart_dataSerializer(data=new_data)
                elif "people" in i:
                    serializer = population_dataSerializer(data=new_data)
                
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
            



@shared_task
def commercial_district_uploaded_file(readLine,country,city):

    header = readLine[0].split(',')
    datas = []

    for k in readLine[1:-1]:
        dict = {name: value for name, value in zip(header, k.split(','))}
        datas.append(dict)

    for data in datas:
        new_data = data.copy()
        new_data["nation"] = country
        new_data["city"] = city
        if not str(new_data["x"]).isdigit():
            new_data['x'] = 0
        else:
            new_data['x'] = int(new_data['x'])

        if not str(new_data["y"]).isdigit():
            new_data['y'] = 0
        else:
            new_data['y'] = int(new_data['y'])
        serializer = commercial_dataSerializer(data=new_data)
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
            print(data)
