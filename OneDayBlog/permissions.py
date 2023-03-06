from rest_framework import permissions
from accounts.models import FollowSystem
from blog.models import Article
class ArticleReadOrWritePermission(permissions.BasePermission):
     def has_permission(self,request,view):
          if request.method in permissions.SAFE_METHODS:
               return True
          else:
           if request.user.is_authenticated:
                return True
     def has_object_permission(self,request,view,obj):
          if obj.user == request.user:
               return True
class LikePermission(permissions.BasePermission):
     def has_permission(self, request, view):
          if request.user.is_authenticated:
               return True
     def has_object_permission(self, request, view, obj):
          if  obj.user != request.user and FollowSystem.objects.filter(to_user=obj.user,user=request.user):
               return True
class FollowRequiredPermission(permissions.BasePermission):
     def has_permission(self, request, view):
          if request.user.is_authenticated:
               return True
     def has_object_permission(self, request, view, obj):
          if FollowSystem.objects.filter(to_user=obj.user,user=request.user).exists():
               return True
