from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Article,CommentSystem,LikeSystem,DisLikeSystem,ActivitySystem
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.utils import timezone



"""
Custom relational fields for user

"""
class UsernameField(serializers.RelatedField):
    def to_representation(self, value):
        user=get_object_or_404(User,username=value)
        username = user.username
        return username


class GetBlogSerializer(serializers.ModelSerializer):
    time_left=serializers.SerializerMethodField()

    user=UsernameField(read_only=True)
    class Meta:
        model=Article
        exclude=['slug']
    comments = serializers.SerializerMethodField()
    def get_time_left(self, obj):
        hours = int(((obj.publish_date + timedelta(days=1)) - datetime.now(tz=timezone.utc)).total_seconds() / (60 * 60))
        return f'{hours} hours left to read this article'
    def get_comments(self,obj):
        comments= obj.comments.filter(is_sub_comment=False)
        return GetCommentSerializer(comments,many=True).data



class PostBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        fields=['title','body','is_private']
class GetCommentSerializer(serializers.ModelSerializer):
    sub_comments = serializers.SerializerMethodField()
    id=serializers.SerializerMethodField()
    likes=serializers.SerializerMethodField()
    dislikes=serializers.SerializerMethodField()
    class Meta:
        model=CommentSystem
        fields=['id','user','body','comment_date','sub_comments','likes','dislikes']
    def get_sub_comments(self,obj):
        sub=obj.sub_comment.filter(is_sub_comment=True, comment=obj)
        return GetCommentSerializer(sub,many=True).data
    def get_id(self,obj):
        id=obj.id
        return id
    def get_likes(self,obj):
        likes = obj.like.all()
        return GetLikeListSerializer(instance=likes, many=True).data
    def get_dislikes(self,obj):
        dislikes = obj.dislike.all()
        return GetDisLikeListSerializer(instance=dislikes, many=True).data

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentSystem
        fields=['body']
class GetLikeListSerializer(serializers.ModelSerializer):
    class Meta:
        model=LikeSystem
        fields=['user']

class GetDisLikeListSerializer(serializers.ModelSerializer):
     class Meta:
        model = DisLikeSystem
        fields = ['user']
class GetActivityListSerializer(serializers.ModelSerializer):
    str_value=serializers.SerializerMethodField()
    class Meta:
        model=ActivitySystem
        fields=['id','str_value']
    def get_str_value(self,obj):
        return str(obj)

        
    