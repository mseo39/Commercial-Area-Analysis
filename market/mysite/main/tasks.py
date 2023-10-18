# mysite/tasks.py

from celery import shared_task
from .models import Commercial_data, Store_data, Sales_data, Population_data
from .serializers import commercial_dataSerializer, store_dataSerializer, sales_dataSerializer, population_dataSerializer,apart_dataSerializer
import logging
logger = logging.getLogger(__name__)

@shared_task
def process_uploaded_file(file_data,country,city):
    logger.error("insert")
    for i, value in file_data.items() :
    
        readLine=value
        header = readLine[0].split(',')

        datas = []

        for k in readLine[1:-1]:
            dict = {name: value for name, value in zip(header, k.split(','))}
            datas.append(dict)

        if "commercial_district" in i:
            for data in datas:
                data["nation"] = country
                data["city"] = city
                if not str(data["x"]).isdigit():
                    data['x'] = 0
                else:
                    data['x'] = int(data['x'])

                if not str(data["y"]).isdigit():
                    data['y'] = 0
                else:
                    data['y'] = int(data['y'])
                serializer = commercial_dataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
                    print(data)
        elif "market" in i:
            for data in datas:
                for key, value in data.items():
                    if key in ['nation','city','commercial_name','service_code','service_name']:
                        continue
                    else:
                        if str(value).isdigit()==False:
                            data[key]=0
                        else:
                            data[key]=int(value)
                try:
                    commercial_instance = Commercial_data.objects.get(
                    nation=country,
                    city=city,
                    commercial_code=data["commercial_code"]
                )
                except Commercial_data.DoesNotExist:
                    print("Commercial_data matching query does not exist:", data)
                    continue

                data["commercial"]=commercial_instance.pk
                
                serializer = store_dataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
        elif "sales" in i:
            for data in datas:
                for key, value in data.items():
                    if key in ['nation','city','service_code','service_name']:
                        continue
                    else:
                        if str(value).isdigit()==False:
                            data[key]=0
                        else:
                            data[key]=int(value)
                try:
                    commercial_instance = Commercial_data.objects.get(
                    nation=country,
                    city=city,
                    commercial_code=data["commercial_code"]
                )
                except Commercial_data.DoesNotExist:
                    print("Commercial_data matching query does not exist:", data)
                    continue

                data["commercial"]=commercial_instance.pk
                
                serializer = sales_dataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
        elif "apart" in i:
            for data in datas:
                for key, value in data.items():
                    if key in ['nation','city']:
                        continue
                    else:
                        if str(value).isdigit()==False:
                            data[key]=0
                        else:
                            data[key]=int(value)
                try:
                    commercial_instance = Commercial_data.objects.get(
                    nation=country,
                    city=city,
                    commercial_code=data["commercial_code"]
                )
                except Commercial_data.DoesNotExist:
                    print("Commercial_data matching query does not exist:", data)
                    continue

                data["commercial"]=commercial_instance.pk
                
                serializer = apart_dataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)
        elif "people" in i:
            for data in datas:
                for key, value in data.items():
                    if key in ['nation','city']:
                        continue
                    else:
                        if str(value).isdigit()==False:
                            data[key]=0
                        else:
                            data[key]=int(value)
                try:
                    commercial_instance = Commercial_data.objects.get(
                    nation=country,
                    city=city,
                    commercial_code=data["commercial_code"]
                )
                except Commercial_data.DoesNotExist:
                    print("Commercial_data matching query does not exist:", data)
                    continue

                data["commercial"]=commercial_instance.pk
                
                serializer = population_dataSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    print(serializer.errors)

            return JsonResponse({'message': 'File upload and data processing completed successfully.'}, status=status.HTTP_201_CREATED)

