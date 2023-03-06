from django.db import models

from django.contrib.auth import get_user_model

class FollowSystem(models.Model):
    user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='follower')
    to_user=models.ForeignKey(get_user_model(),on_delete=models.CASCADE,related_name='following')
    follow_date=models.DateTimeField(auto_now_add=True)
    
    def __iter__(self):
        return iter(self.to_user)

    def __str__(self):
        return f'{self.user} followed {self.to_user}'
    