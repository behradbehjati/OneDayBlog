from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import FollowSystem

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=100)
    password=serializers.CharField(max_length=100)


        

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs = {'password': {'write_only': True}}
        

        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'], validated_data['email'],
                                            validated_data['password'])

            return user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email']
        
        
        
class UsernameField(serializers.RelatedField):
    def to_representation(self, value):
        user=get_object_or_404(User,username=value)
        username = user.username
        return username
class GetFollowSerializer(serializers.ModelSerializer):
    user = UsernameField(read_only=True)
    class Meta:
        model=FollowSystem
        fields=['user']
    

    
