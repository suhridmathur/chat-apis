from django.db import models
from django.contrib.auth.models import User

class Thread(models.Model):
    first = models.ForeignKey(User, on_delete=models.CASCADE, related_name='first_user')
    second = models.ForeignKey(User, on_delete=models.CASCADE, related_name='second_user')


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)