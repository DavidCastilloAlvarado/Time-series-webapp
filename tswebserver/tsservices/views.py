# Create your views here.
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from django.shortcuts import render, redirect
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated,AllowAny

from tswebserver.utils.forecast import ForecastTask
from .models import Product
from .serializers import ForecastIncomeSerializer

FORECASTTASK = ForecastTask()

class HomeView(GenericAPIView):
    database = FORECASTTASK

    def get(self, request):
        data = self.database.articulos.to_dict(orient='records')
        context = dict(articulos=data)
        return render(request, 'home/home.html', context)

@method_decorator(cache_page(60*60*1), name='forecast')
class ForescastApiView(ViewSet):
    queryset = Product.objects.all()
    serializer_class = ForecastIncomeSerializer
    forecast_model = FORECASTTASK

    @action(detail=False, methods=['GET', ],)
    def forecast(self, request):
        income = self.serializer_class(data = request.GET)
        income.is_valid(raise_exception=True)
        before, prediction = self.forecast_model.forecast(income.data.get('id_articulo'),
                                                income.data.get('t_ahead'))
        # TODO: Create a function to calculate the forecast
        return Response({"before":before, "pred":prediction}, status=status.HTTP_200_OK)

homeview = HomeView.as_view()