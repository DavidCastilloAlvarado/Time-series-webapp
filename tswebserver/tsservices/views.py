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
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from tswebserver.utils.forecast import ForecastTask, BasketAnalysis
from tswebserver.tsservices.models import Product
from .serializers import ForecastIncomeSerializer

from django.contrib.auth.decorators import login_required

FORECASTTASK = ForecastTask()
BASKETA = BasketAnalysis()


class HomeView(GenericAPIView):
    database = FORECASTTASK

    def get(self, request):
        # data = self.database.articulos.to_dict(orient='records')
        # context = dict(articulos=data)
        return render(request, 'home/homeempty.html',)


@login_required()
def homeforescast(request):
    data = FORECASTTASK.articulos.to_dict(orient='records')
    context = dict(articulos=data)
    return render(request, 'home/home.html', context)


@method_decorator(cache_page(60*60*1), name='forecast')
class ForescastApiView(ViewSet):
    queryset = Product.objects.all()
    serializer_class = ForecastIncomeSerializer
    forecast_model = FORECASTTASK
    basket_analysis = BASKETA

    @action(detail=False, methods=['GET', ],)
    def forecast(self, request):
        income = self.serializer_class(data=request.GET)
        income.is_valid(raise_exception=True)
        # try:
        related_articulos = self.basket_analysis.get_items_related(
            income.data['id_articulo'])
        data_forecast, ahead, name = self.forecast_model.forecast(income.data.get('id_articulo'),
                                                                  income.data.get('t_ahead'))
        return Response({"data": data_forecast, "ahead": ahead, "name": name, "related": related_articulos}, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response(dict(error=str(e)), status=status.HTTP_400_BAD_REQUEST)


homeview = HomeView.as_view()
