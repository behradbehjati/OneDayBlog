from django.urls import path,include
from . import views
from rest_framework import routers
app_name='blog'
'''
    can even change the like and dislike to upvote and downvote
'''
urlpatterns=[
    path('home/articles/',views.ArticleFeedApiView.as_view(),name='feed'),
    path('home/activities/',views.ActivityFeedApiView.as_view(),name='activity'),
    path('blog/<int:id>/',include([
        path('like/',views.AddLikeApiView.as_view(),name='like'),
        path('like/comment/<int:comment_id>/',views.AddLikeApiView.as_view(),name='like'),
        path('dislike/', views.DisLikeApiView.as_view(), name='dislike'),
        path('dislike/comment/int:comment_id>/', views.DisLikeApiView.as_view(), name='dislike'),
        path('comment/<int:comment_id>/', views.AddCommentApiView.as_view(), name='comment'),
        path('comment/', views.AddCommentApiView.as_view(), name='comment'),


    ]))]

router = routers.SimpleRouter()
router.register('blog', views.BlogViewSet,basename='blog')
urlpatterns += router.urls