from django.contrib import admin
from .models import Article,LikeSystem,DisLikeSystem,CommentSystem,ActivitySystem

class ArticleAdmin(admin.ModelAdmin):
    ordering=['-publish_date']
    list_display=['title','user','publish_date']
    search_fields=['user','title']
    list_filter=['user','title']
admin.site.register(Article,ArticleAdmin)
class LikeSystemAdmin(admin.ModelAdmin):
    ordering=['-like_date']
    list_display=['user','content_object']
admin.site.register(LikeSystem,LikeSystemAdmin)

class DisLikeSystemAdmin(admin.ModelAdmin):
    ordering=['-dislike_date']
    list_display=['user','content_object']
admin.site.register(DisLikeSystem,DisLikeSystemAdmin)
class CommentSystemAdmin(admin.ModelAdmin):
    ordering=['-comment_date']

admin.site.register(CommentSystem,CommentSystemAdmin)
class ActivitySystemAdmin(admin.ModelAdmin):
    list_display = ['user','action','content_object']
admin.site.register(ActivitySystem, ActivitySystemAdmin)

