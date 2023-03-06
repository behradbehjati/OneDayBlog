from django.contrib.auth import login,authenticate,logout
from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework import generics, permissions
from rest_framework.views import APIView
from .serializers import LoginSerializer,RegisterSerializer,UserSerializer,GetFollowSerializer
from blog.serializers import GetBlogSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import FollowSystem
from blog.models import Article



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginApiView(generics.GenericAPIView):
    serializer_class=LoginSerializer
    def post(self,request,*args,**kwargs):

        ser_data=self.get_serializer(data=request.POST)
        if ser_data.is_valid():
            user=authenticate(username=ser_data.validated_data['username'],password=ser_data.validated_data['password'])

            login(request,user)
            tokens = get_tokens_for_user(user)
            request.session['jwt']=tokens
            print(request.session['jwt'])
            return Response({'message':'logged in successfully','tokens': tokens})
        return Response(ser_data.errors)

class RegisterApiView(generics.GenericAPIView):
    
    serializer_class=RegisterSerializer
    def post(self, request, *args, **kwargs):
        ser_data = self.get_serializer(data=request.data)
        if ser_data.is_valid():
            user=User.objects.create_user(
                username=ser_data.validated_data['username'],email=ser_data.validated_data['email'],password=ser_data.validated_data['password']
            )


            return Response({'user':UserSerializer(user,context=self.get_serializer_context(),).data})

        return Response(ser_data.errors)
class LogoutApiView(APIView):
    def get(self,request):
        logout(request)
        del request.session['jwt']
        return Response({'message':'logged out successfully'})
class FollowCreateApiView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,id):
        to_user=get_object_or_404(User,id=id)
        user=request.user 
        FollowSystem.objects.get_or_create(user=user,to_user=to_user)
        return Response({'message':f'you followed {to_user}'})
class UnFollowApiView(APIView):
    def post(self,request,id):
        to_user=get_object_or_404(User,id=id)
        user=request.user
        FollowSystem.objects.get(to_user=to_user,user=user).delete()
        return Response({'message':f'you unfollowed {to_user}'})
class DashboardApiView(APIView):

    permission_classes=[IsAuthenticated]
    def get(self,request,id):
        user=User.objects.get(id=id)
        articles=Article.objects.filter(user=id)
        followers=user.following.all()
        print(followers)
        ser_follow=GetFollowSerializer(instance=followers)
        ser_articles=GetBlogSerializer(instance=articles,many=True)
        return Response({'articles':ser_articles.data,'followers':ser_follow.data})







        

    
        