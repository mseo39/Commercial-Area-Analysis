from rest_framework import serializers
from main.models import Commercial_data, Store_data,Sales_data,Apart_data,Population_data

class commercial_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commercial_data
        fields='__all__'

class store_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store_data
        fields='__all__'

class sales_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sales_data
        fields='__all__'

class apart_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Apart_data
        fields='__all__'

class population_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model=Population_data
        fields='__all__'