from rest_framework import serializers
from django.conf import settings

class ForecastIncomeSerializer(serializers.Serializer):
    id_articulo = serializers.CharField(max_length=200)
    t_ahead = serializers.IntegerField(max_value = 6, default = 1)


