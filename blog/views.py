from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializer import *
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .permissions import CustomModelPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters,status
from rest_framework.parsers import MultiPartParser, FormParser

# Create your views here.
@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user= authenticate(username=email,password=password)
    if user == None:
        return Response('user not found')
    else:
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'token':token.key})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register(request):
    password = request.data.get('password')
    group_id = request.data.get('group')
    blog_id = request.data.get('Blog')  # Get company_info ID from request data

    try:
        group_object = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response({'error': 'No such group!'})

    hash_password = make_password(password)

    # Set company_info field directly using the ID from the request data
    request.data['password'] = hash_password
    request.data['Blog'] = blog_id

    serializer = UserInfoSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        user.groups.add(group_object.id)
        user.save()
        return Response({'data': 'User created!'})
    else:
        return Response({'error': serializer.errors})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def admin_create(request):
    password = request.data.get('password')
    try:
        group_object = Group.objects.get(name='Admin')
    except:
        return Response({'error':'No such groups!'})
    hash_password = make_password(password)
    request.data['password'] = hash_password
    serializer = UserInfoSerializer(data = request.data)
    if serializer.is_valid():
        user = serializer.save()
        user.groups.add(group_object.id)
        user.save()
        return Response({'data':'Admin created!'})
    else:
        return Response({'error':serializer.errors})


class CategoryApiView(GenericAPIView):
    queryset_model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']
    permission_classes = [IsAuthenticated,CustomModelPermission]
    def get(self,request):
        category_objects = self.get_queryset()
        filter_object = self.filter_queryset(category_objects)
        serializer = CategorySerializer(filter_object,many=True)
        return Response({'data':serializer.data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data created.'})
        else:
            return Response({'error':serializer.errors})
        
class CategoryIdApiView(GenericAPIView):
    queryset_model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request,pk):
        try:
            category_object = Category.objects.get(id=pk)
        except:
            return Response({'data':'Data not found!'})
        serializer = CategorySerializer(category_object)
        return Response(serializer.data)
    
    def put(self, request, pk):
        try:
            category_objects = Category.objects.get(id=pk)
        except:
            return Response({'data':'data not found!'})
        serializer = CategorySerializer(category_objects,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data updated successfully!'})
        else:
            return Response(serializer.errors)
        
    def delete(self,request, pk):
        try:
            category_objects = Category.objects.get(id=pk)
        except:
            return Response('Data not found!')
        category_objects.delete()
        return Response({'Data':'data deleted successfully!'})
    
class BlogApiView(GenericAPIView):
    queryset_model = Blog
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields = ['title']
    search_fields = ['title','discription','category']
    permission_classes = [IsAuthenticated,CustomModelPermission]


    def get(self,request):
        blog_objects = self.get_queryset()
        filter_objects = self.filter_queryset(blog_objects)
        serializer = BlogSerializer(filter_objects,many=True)
        return Response({'data':serializer.data})

    def post(self,request):
        serializer =BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':'data Created.'})
        else:
            return Response({'error':serializer.errors})
    
    
    
        
    
class BlogIdApiView(GenericAPIView):
    queryset_model = Blog
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request,pk):
        try:
            blog_object = Blog.objects.get(id=pk)
        except:
            return Response({'data':'Data not found!'})
        serializer = BlogSerializer(blog_object)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            blog_object = Blog.objects.get(id=pk)
        except:
            return Response({'Data':'Data not found!'})
        serializer = BlogSerializer(blog_object,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Data':'Data updated successfully'})
        else:
            return Response(serializer.errors)
        
    def delete(self,request,pk):
        try:
            blog_object = Blog.objects.get(id=pk)
        except:
            return Response({'Data':'Data not found!'})
        blog_object.delete()
        return Response({'Data':'Data deleted successfully!'})



class GroupApiView(GenericAPIView):
    queryset_model = Group
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated,CustomModelPermission]

    def get(self,request):
        group_objects = self.get_queryset()
        serializer = self.serializer_class(group_objects,many=True)
        return Response({'data':serializer.data})