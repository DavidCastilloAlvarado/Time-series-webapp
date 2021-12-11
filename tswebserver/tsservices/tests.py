from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
import time
from io import StringIO
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from tswebserver.utils.forecast import ForecastTask, BasketAnalysis


class MultiTestTsServicesCases(TestCase):

    def setUp(self):
        self.userdata = {'username': 'admintest',
                         'email': 'admin@admintest.com',
                         'password': 'admintest'}

    def test_landing_page_response(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home/homeempty.html')
        self.assertContains(response, 'Welcome to the TS Web Server')
        self.assertContains(response, 'DMPMLG - Pronóstico de la demanda')

    def test_admin_page_render(self):
        response = self.client.get('/admin/', follow=True)
        self.assertContains(response, 'Django administration')

    def test_forecasting_class_data_reading(self,):
        FORECASTTASK = ForecastTask()
        # BASKETA = BasketAnalysis()
        data = FORECASTTASK.articulos.to_dict(orient='records')
        data_item = data[0]
        self.assertTrue('idArticulo' in data_item)
        self.assertTrue('DescProducto' in data_item)

    def test_forecasting_class_forescast(self,):
        FORECASTTASK = ForecastTask()
        # BASKETA = BasketAnalysis()
        data = FORECASTTASK.articulos.to_dict(orient='records')
        data_item = data[0]
        ahead_ = 2
        response, ahead, name = FORECASTTASK.forecast(
            str(data_item['idArticulo']), ahead_)
        self.assertTrue('labels' in response)
        self.assertTrue(name in data_item['DescProducto'])
        self.assertTrue(ahead == ahead_)
