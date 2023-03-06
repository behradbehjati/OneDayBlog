from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType

class Article(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,name='user')
    title=models.CharField(max_length=200,unique=True)
    body=models.TextField()
    slug=models.SlugField()
    is_private=models.BooleanField(default=False)
    publish_date=models.DateTimeField(auto_now_add=True)
    update_date=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user}-{self.title:50}'
    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('aticle', kwargs={'pk': self.pk})


"""
delete this like model after deleting the database , there was migration issue and name 

"""
class Like(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,name='like',related_name='like')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    like_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.like} liked {self.content_object}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),

        ]

class LikeSystem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='likes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    like_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} liked {self.content_object}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]

class DisLikeSystem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='dislikes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    dislike_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.user} disliked {self.content_object}'

    class Meta:
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
        ]
class CommentSystem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comments')
    body=models.CharField(max_length=300)
    article=models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    is_sub_comment=models.BooleanField(default=False)
    comment=models.ForeignKey('CommentSystem',blank=True,null=True,on_delete=models.CASCADE,related_name='sub_comment')
    comment_date=models.DateTimeField(auto_now_add=True)
    like=GenericRelation(LikeSystem)
    dislike=GenericRelation(DisLikeSystem)
    def __str__(self):
        return f'{self.user} commented on {self.article}'

    class Meta:
        indexes = [
            models.Index(fields=["user", "article"]),
        ]
class ActivitySystem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='activity')
    action=models.CharField(max_length=150)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    action_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.action} {self.content_object}'

    class Meta:
        indexes = [
            models.Index(fields=["user", "action"]),
        ]





