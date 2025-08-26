from django.db import models
from django.contrib.auth.models import User

class chatGroup(models.Model):
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.group_name
    
class groupMessage(models.Model):
    group = models.ForeignKey(chatGroup, on_delete=models.CASCADE, related_name='chat_messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.body}'
    class Meta:
        ordering = ['-created']