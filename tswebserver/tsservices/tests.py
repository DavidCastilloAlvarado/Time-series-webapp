from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
import time
from io import StringIO
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from tswebserver.utils.forecast import ForecastTask, BasketAnalysis
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.test import tag

USER_DATA = {'username': 'admintest',
             'email': 'admin@admintest.com',
             'password': 'admintest'}


class MultiTestTsServicesCases(TestCase):

    def setUp(self):
        self.userdata = USER_DATA

    def login_user(self):
        response = self.client.post('/accounts/login/',
                                    {'username': self.userdata['username'],
                                     'password': self.userdata['password'], })
        return response

    def create_super_user(self):
        my_admin = User.objects.create_superuser(self.userdata['username'],
                                                 self.userdata['email'],
                                                 self.userdata['password'], )
        return my_admin

    @tag('frontend', 'unitario', ))
    def test_landing_page_response(self):
        response=self.client.get('/')
        self.assertTemplateUsed(response, 'home/homeempty.html')
        self.assertContains(response, 'Welcome to the TS Web Server')
        self.assertContains(response, 'DMPMLG - Pronóstico de la demanda')

    @ tag('frontend', 'unitario', ))
    def test_admin_page_render(self):
        response=self.client.get('/admin/', follow=True)
        self.assertContains(response, 'Django administration')

    # Forecasting
    @ tag('backend', 'unitario')
    def test_forecasting_class_data_reading(self,):
        FORECASTTASK=ForecastTask()
        # BASKETA = BasketAnalysis()
        data=FORECASTTASK.articulos.to_dict(orient='records')
        data_item=data[0]
        self.assertTrue('idArticulo' in data_item)
        self.assertTrue('DescProducto' in data_item)

    @ tag('backend', 'unitario')
    def test_forecasting_class_forescast(self,):
        FORECASTTASK=ForecastTask()
        # BASKETA = BasketAnalysis()
        data=FORECASTTASK.articulos.to_dict(orient='records')
        data_item=data[0]
        ahead_=2
        response, ahead, name=FORECASTTASK.forecast(
            str(data_item['idArticulo']), ahead_)

        self.assertTrue('labels' in response)
        self.assertTrue(name in data_item['DescProducto'])
        self.assertTrue(ahead == ahead_)

    # Basket analysis
    @ tag('backend', 'unitario')
    def test_basket_analysis_class_data_reading(self,):
        BASKETA=BasketAnalysis()
        data=BASKETA.table.to_dict(orient='records')
        data_item=data[0]

        self.assertTrue('antecedents' in data_item)
        self.assertTrue('idArticulo' in data_item)

    @ tag('backend', 'unitario')
    def test_basket_analysis_class_related_articulos(self,):
        BASKETA=BasketAnalysis()
        data=BASKETA.table.to_dict(orient='records')
        data_item=data[0]

        related=BASKETA.get_items_related(data_item['antecedents'])

        self.assertTrue(type(related) == list)

    # Forecasting API
    @ tag('backend', 'integración')
    def test_forecasting_API(self,):
        user=self.create_super_user()
        response=self.login_user()

        FORECASTTASK=ForecastTask()
        # BASKETA = BasketAnalysis()
        data=FORECASTTASK.articulos.to_dict(orient='records')
        data_item=data[0]
        ahead_=2
        data={
            'id_articulo': str(data_item['idArticulo']),
            't_ahead': ahead_
        }
        response=self.client.get('/api/model/forecast/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(type(response.data['data']) == dict)
        self.assertTrue(response.data['ahead'] == ahead_)
        self.assertTrue(response.data['name'] == data_item['DescProducto'])
        self.assertTrue(type(response.data['related']) == list)


class UserInterfaceTests(StaticLiveServerTestCase, TestCase):
    # fixtures = ['user-data.json']
    @ classmethod
    def setUp(self):
        self.located=False
        my_admin=User.objects.create_superuser(self.userdata['username'],
                                                 self.userdata['email'],
                                                 self.userdata['password'], )

    @ classmethod
    def setUpClass(self,):
        super().setUpClass()
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # open Browser in maximized mode
        chrome_options.add_argument("--start-maximized")

        chrome_options.add_argument("--disable-gpu")
        self.userdata=USER_DATA
        self.selenium=webdriver.Chrome(options=chrome_options)
        self.selenium.implicitly_wait(10)

    @ classmethod
    def tearDownClass(self):
        self.selenium.quit()
        super().tearDownClass()

    @ tag('integración', 'frontend')
    def test_login(self):
        # user = self.create_super_user()
        # self.assertTrue(User.objects.filter(
        #     username=user.username).exists())

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login/'))
        username_input=self.selenium.find_element_by_name("username")
        username_input.send_keys(self.userdata['username'])
        password_input=self.selenium.find_element_by_name("password")
        password_input.send_keys("self.userdata['password']")

        # self.selenium.save_screenshot('screenshot.png')
        self.selenium.find_element_by_xpath(
            '/html/body/center/div/div/form/button').click()
        time.sleep(1)
        self.assertTrue(self.selenium.current_url !=
                        self.live_server_url+'/dashboard/main/')

    @ tag('integración', 'frontend')
    def test_dashboard(self):
        # user = self.create_super_user()
        # self.assertTrue(User.objects.filter(
        #     username=user.username).exists())

        self.selenium.get('%s%s' % (self.live_server_url, '/dashboard/main/'))
        # self.selenium.save_screenshot('screenshot.png')
        if self.located:
            self.selenium.find_element_by_xpath(
                '/html/body/div[2]/div/div[1]/div/div[1]').click()
            self.selenium.find_element_by_xpath(
                '/html/body/div[2]/div/div[2]/div/canvas')
        time.sleep(8)
        self.assertTrue(self.selenium.current_url !=
                        self.live_server_url+'/dashboard/main/')
