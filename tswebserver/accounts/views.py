from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .serializers import User_Serializers, Userlog_Serializers
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
# Create your views here.


def home_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'accounts/login')


class Login_view(GenericAPIView):
    serializer_class = Userlog_Serializers

    def post(self, request):
        #form = AuthenticationForm(data=request.POST)
        serializer = self.serializer_class(data=request.data,
                                           request=request)

        if serializer.is_valid():
            login(request,
                  serializer.user_cache,
                  backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/dashboard/main/')
        return render(request, 'accounts/login.html', {'status': serializer.errors})

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'accounts/login.html')


# class Register_View(GenericAPIView):
#     serializer_class = User_Serializers

#     def get(self, request):
#         if request.user.is_authenticated:
#             return redirect('/rss/user')
#         return render(request, 'accounts/signup.html')

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             username = serializer.validated_data.get("username")
#             password = serializer.validated_data.get("password")
#             user = authenticate(request, username=username, password=password)
#             login(request, user)
#             return redirect('/rss/user')
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # print(serializer.errors)
#         return render(request, 'accounts/signup.html', {'status': serializer.errors})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/accounts/login')
