from django.test import TestCase
from rssapp.utiles import get_rss_link, get_items_from_feed
from rssapp.serializer import Add_feed_user, Id_feed_serializer, log_serializer
from accounts.serializers import User_Serializers
from rest_framework.test import APITestCase
from rssapp.models import User_feed, log_errors
from django.contrib.auth.models import User
from rest_framework import status
import time


class MultiTestAccountCases(TestCase):

    def setUp(self):
        self.userdata = {'username': 'dave5',
                         'first_name': 'david',
                         'last_name': 'castillo',
                         'email': 'dcastilloa@uni.pe',
                         'password_1': 'TnLM17gr9nFNQnl',
                         'password_2': 'TnLM17gr9nFNQnl', }
        self.bad_userdata = self.userdata.copy()
        self.bad_userdata['password_2'] = 'TnLM17gr9nFN'

    def signup_user(self, mode='good'):
        if mode == 'good':
            request = self.client.post('/accounts/signup/', self.userdata)
        elif mode == 'fail':
            request = self.client.post('/accounts/signup/', self.bad_userdata)
        return request

    def login_user(self):
        response = self.client.post('/accounts/login/',
                                    {'username': self.userdata['username'],
                                     'password': self.userdata['password_2'], })
        return response

    def user_signup_login(self):
        response = self.signup_user()
        response = self.login_user()
        return response

    def test_user_signup_serializer(self,):
        """
        Test if the serializer for signup works properly
        """
        serializer = User_Serializers(data=self.userdata)
        self.assertTrue(serializer.is_valid())

    def test_signup_user(self,):
        """
        This test need a server running
        Test the signup user api, test end to end
        - post request
        - serializer 
        - save into model
        - verify if the user is registered
        """
        request = self.signup_user()

        self.assertTrue(User.objects.filter(
            username=self.userdata['username']).exists())

    def test_signup_user_fail(self,):
        """
        This test need a server running
        Test the signupapi but using a bad request, password mismatch
        - post request to signup
        - serializar validate
        - verify that the user is not registered
        """
        request = self.signup_user(mode='fail')

        self.assertTrue(not User.objects.filter(
            username=self.bad_userdata['username']).exists())

    def test_login_user(self,):
        """"
        This test need a server running
        Test the signup user api, test end to end
        - post request
        - serializer validated
        - save into user model
        Test the login user api, test end to end
        - post request
        - serializer validated
        verify if the user exist
        verify that the user is in the user home page
        """
        response = self.user_signup_login()
        response = self.client.get("/rss/user/")
        self.assertTrue(User.objects.filter(
            username=self.userdata['username']).exists())
        self.assertContains(response, 'Hello dave5')

    def test_home_template(self):
        """
        For unsignup clients, the other pages are block,
        so his home page has to be account/home.html
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, "accounts/home.html")

    def test_unauthorize_user_home(self):
        """
        For unsignup clients, the other pages are block,
        so any attempt to accest to unauthorize page
        the server going to redirect to account/home.html
        """
        response = self.client.get('/rss/user/', follow=True)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_unauthorize_user_adding(self):
        """
        For unsignup clients, the other pages are block,
        so any attempt to accest to unauthorize page
        the server going to redirect to account/home.html
        """
        response = self.client.get('/rss/adding/', follow=True)
        self.assertTemplateUsed(response, "accounts/login.html")
