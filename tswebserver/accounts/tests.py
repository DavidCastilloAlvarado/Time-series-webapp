from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
import time
from io import StringIO
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError


class MultiTestAccountCases(TestCase):

    def setUp(self):
        self.userdata = {'username': 'admintest',
                         'email': 'admin@admintest.com',
                         'password': 'admintest'}

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

    def test_create_superuser(self,):
        """
        Testea si se creo un superusuario apropiadamente
        """
        user = self.create_super_user()
        # self.client.login(username=user.username, password=user.password)
        self.assertTrue(User.objects.filter(
            username=user.username).exists())

    def test_user_login(self,):
        user = self.create_super_user()
        response = self.login_user()
        response = self.client.get('/dashboard/main/', follow=True)
        self.assertTemplateUsed(response, 'home/home.html')

    def test_user_login_fail(self,):
        response = self.client.post('/accounts/logout/')
        response = self.client.post('/accounts/login/',
                                    data={'username': 'anotherthing',
                                          'password': 'anotherthing', })
        self.assertContains(response, 'Login')

    def test_access_without_login(self,):
        response = self.client.post('/accounts/logout/')
        response = self.client.get('/dashboard/main/', follow=True)
        self.assertContains(response, 'Login')

    def test_login_page_render(self,):
        response = self.client.get('/accounts/login/', follow=True)
        self.assertContains(response, 'Login')
        self.assertContains(response, 'DMPMLG - Pronóstico de la demanda')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Please put your username')
        self.assertContains(response, 'Password')
