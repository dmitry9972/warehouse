from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from main.models import  Order
from rest_framework.generics import RetrieveAPIView, CreateAPIView, ListAPIView
from .serializers import RegistrationSerializer, OrderSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView

from rest_framework.permissions import AllowAny

@permission_classes((AllowAny,))
class registration_view(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['response']= "succesfully registered a new user"
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token']=token
        else:
            data = serializer.errors
        return Response(data)

@permission_classes((IsAuthenticated,))
@authentication_classes([TokenAuthentication, ])
class OrderCreateView(CreateAPIView):

    def post(self, request):


        serializer = OrderSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            serializer.save()
            data['response']= "succesfully registered a new order"
        else:
            data = serializer.errors
        return Response(data)

class order(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by('-order_number')