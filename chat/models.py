from django.contrib.auth import get_user_model
from django.db import models
# Create your models here.

User=get_user_model()

class Message(models.Model):
    author=models.ForeignKey(User, related_name="author_message", on_delete=models.CASCADE)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    reciver=models.ForeignKey(User,null=True,blank=True,related_name="reciver_message", on_delete=models.CASCADE)
    def __str__(self):
        return self.author.username
    
    def last_10_messages(self):
        return Message.objects.order_by('-timestamp').all()[::-1]

    def get_messages(from_user,to_user):
        f1=Message.objects.filter(author=from_user,reciver=to_user)
        f2=Message.objects.filter(author=to_user,reciver=from_user)
        f3=f1.union(f2)
        return f3.order_by("-timestamp")[::-1]

