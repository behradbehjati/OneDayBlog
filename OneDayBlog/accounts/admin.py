from django.contrib import admin
from .models import FollowSystem

class FollowSystemAdmin(admin.ModelAdmin):
    ordering=['-follow_date']
    list_display=['user','to_user','follow_date']
admin.site.register(FollowSystem,FollowSystemAdmin)