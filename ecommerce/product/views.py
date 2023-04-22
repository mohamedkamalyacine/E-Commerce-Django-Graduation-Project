import datetime
from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, mixins, generics
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

# imports for user credentials
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserSerializer
# Create your views here.

#  User authentication should be implemented using token-based authentication,
#  and the tokens should expire after an hour

# class AuthView(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request':request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})






# TOKEN_TTL = datetime.timedelta(hours=1)

# @api_view(['POST'])
# @csrf_exempt
# def login(request):
#     username = request.POST.get('username')
#     password = request.POST.get('password')
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         token, created = Token.objects.get_or_create(user=user)
#         token.expires = datetime.datetime.now() + TOKEN_TTL
#         token.save()
#         return Response({'token': token.key})
#     else:
#         return Response({'error': 'Invalid credentials'})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def protected(request):
#     content = {'message': 'You are authenticated'}
#     return Response(content)



class AuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# Users should be able to browse products by categories and search for specific products using keywords.

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']


# Categories should be managed through DRF's API endpoints.


# Products should be able to be added, edited and deleted through DRF's API endpoints
class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



# Products should be able to be added, edited and deleted through DRF's API endpoints.
# class GenericProductAdd(generics.CreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]
    
# class GenericProductDestroy(generics.DestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]

# class GenericProductUpdate(generics.UpdateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAuthenticated]
    
class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



# class GenericProductList(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.AllowAny]
#     # authentication_class = [JWTAuthentication]
#     # pagination_class = StandardResultsSetPagination


# 6- Users should be able to create an account, update their profile, and view their order history through DRF's API endpoints.
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class OrderHistory(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
# ===============================================================
class UserInformationView(generics.CreateAPIView):
    serializer_class = UserInformationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_info = UserInformation.objects.create(
            user=request.user,
            name=serializer.validated_data['name'],
            email=serializer.validated_data['email'],
            phone_number=serializer.validated_data['phone_number']
        )
        return Response(serializer.data)

class ShippingDetailsView(generics.CreateAPIView):
    serializer_class = ShippingDetailsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shipping_details = ShippingDetails.objects.create(
            user=request.user,
            address=serializer.validated_data['address'],
            city=serializer.validated_data['city'],
            state=serializer.validated_data['state'],
            country=serializer.validated_data['country'],
            zip_code=serializer.validated_data['zip_code']
        )
        return Response(serializer.data)

class PaymentInformationView(generics.CreateAPIView):
    serializer_class = PaymentInformationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        payment_info = PaymentInformation.objects.create(
            user=request.user,
            card_number=serializer.validated_data['card_number'],
            expiration_month=serializer.validated_data['expiration_month'],
            expiration_year=serializer.validated_data['expiration_year'],
            cvv=serializer.validated_data['cvv']
        )
        return Response(serializer.data)