from django.shortcuts import render,get_object_or_404
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from .models import Article,LikeSystem,DisLikeSystem,CommentSystem,ActivitySystem
from accounts.models import FollowSystem
from rest_framework.views import APIView
from .serializers import GetBlogSerializer,PostBlogSerializer,PostCommentSerializer,GetActivityListSerializer
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,BasePermission, DjangoModelPermissionsOrAnonReadOnly
from permissions import ArticleReadOrWritePermission,LikePermission,FollowRequiredPermission
from rest_framework.pagination import PageNumberPagination



class BlogViewSet(viewsets.ViewSet):

    query_set=Article.objects.all()
    permission_classes=[ArticleReadOrWritePermission,FollowRequiredPermission]
    def list(self,request):
        ser_data=GetBlogSerializer(instance=self.query_set,many=True)
        return Response(ser_data.data,status=status.HTTP_200_OK)
    def create(self,request):
        ser_data=PostBlogSerializer(data=request.POST)
        if ser_data.is_valid():

        
            ser_data.save(user=request.user)
            article=Article.objects.get(user=request.user,title=request.POST['title'])
            ActivitySystem.objects.create(user=request.user,action='created',content_object=article)
            return Response(ser_data.data,status=status.HTTP_200_OK)
        return Response(ser_data.errors,status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self,request,pk):
        article=get_object_or_404(Article,pk=pk)
        if article.is_private==True  :
            if FollowSystem.objects.filter(to_user=article.user,user=request.user).exists() or request.user==article.user:
                ser_data=GetBlogSerializer(instance=article)
                return Response(ser_data.data)
            return Response({'you should follow first'})
        ser_data = GetBlogSerializer(instance=article)
        return Response(ser_data.data)
    def partial_update(self,request,pk):
        article=get_object_or_404(Article,pk=pk)
        ser_data=PostBlogSerializer(instance=article,partial=True,data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            ActivitySystem.objects.create(user=request.user, action='updated', content_object=article)
            return Response(ser_data.data)
        return Response(ser_data.errors)
    def destroy(self,request,pk):
        article = get_object_or_404(Article, pk=pk).delete()
        ActivitySystem.objects.create(user=request.user, action='deleted', content_object=article)
        return Response({'succesfully deleted'})
class ArticleFeedApiView(APIView, PageNumberPagination):
    page_size = 3
    queryset=Article.objects.all()
    permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
    def get(self,request):



        if  request.user.is_authenticated  :
            following = request.user.follower.all().values_list('to_user').get()
            articles = Article.objects.filter(user__in=following)
            if not articles:
                articles=Article.objects.all()
        articles=articles=Article.objects.all()
        results = self.paginate_queryset(articles, request, view=self)
        ser_data=GetBlogSerializer(results,many=True)
        return self.get_paginated_response(ser_data.data)
class ActivityFeedApiView(APIView, PageNumberPagination):
    page_size = 3
    queryset=ActivitySystem.objects.all()
    permission_classes=[DjangoModelPermissionsOrAnonReadOnly]
    def get(self,request):
        following = request.user.follower.all().values_list('to_user').get()

        if  request.user.is_authenticated and following :
            activities = ActivitySystem.objects.filter(user__in=following)

        activities=ActivitySystem.objects.all()
        results = self.paginate_queryset(activities, request, view=self)
        ser_data=GetActivityListSerializer(results,many=True)
        return self.get_paginated_response(ser_data.data)
class AddLikeApiView(APIView):
    permission_classes = [LikePermission]
    def post(self,request,*args,**kwargs):
        article = get_object_or_404(Article, id=kwargs['id'])
        if 'comment_id' in kwargs:
                comment=CommentSystem.objects.get(id=kwargs['comment_id'])
                like=LikeSystem.objects.create(user=request.user, content_object=comment)
                ActivitySystem.objects.create(user=request.user, action='liked', content_object=like)
                self.check_object_permissions(request, article)
                return Response({f'you liked {comment}'})




        else:

                like=LikeSystem.objects.create(user=request.user,content_object=article)
                ActivitySystem.objects.create(user=request.user, action='liked', content_object=like)
                self.check_object_permissions(request, article)
                return Response({f'you liked {article}'})
class DisLikeApiView(APIView):

    permission_classes = [LikePermission]
    def post(self,request,*args,**kwargs):

        article = get_object_or_404(Article, id=kwargs['id'])
        if 'comment_id' in kwargs:
            comment = CommentSystem.objects.get(id=kwargs['comment_id'])
            dislike=DisLikeSystem.objects.create(user=request.user, content_object=comment)
            ActivitySystem.objects.create(user=request.user, action='disliked', content_object=dislike)
            self.check_object_permissions(request, article)
            return Response({f'you disliked {comment}'})




        else:

            dislike=DisLikeSystem.objects.create(user=request.user, content_object=article)
            ActivitySystem.objects.create(user=request.user, action='disliked', content_object=dislike)
            self.check_object_permissions(request, article)
            return Response({f'you disliked {article}'})

class AddCommentApiView(APIView):
    permission_classes = [FollowRequiredPermission]
    def post(self,request,*args,**kwargs):
        ser_data=PostCommentSerializer(data=request.data)
        if ser_data.is_valid():
             try :
                comment=CommentSystem.objects.create(user=request.user,article=Article.objects.get(id=kwargs['id']),body=ser_data.validated_data['body'],is_sub_comment=True,
                                             comment=CommentSystem.objects.get(id=kwargs['comment_id']))
                ActivitySystem.objects.create(user=request.user, action='comment', content_object=comment)
                return Response({'you commented'})
             except:
                comment=CommentSystem.objects.create(user=request.user,article=Article.objects.get(id=kwargs['id']),body=ser_data.validated_data['body'])
                ActivitySystem.objects.create(user=request.user, action='commented', content_object=comment)
                return Response({'you commented'})
        return Response(ser_data.errors)

            


            
            
    


        

