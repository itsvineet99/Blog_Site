from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    like = models.ManyToManyField(User, related_name="like")
    dislike = models.ManyToManyField(User, related_name="dislike")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})
    
    def total_likes(self):
        return self.like.count()
    def total_dislikes(self):
        return self.dislike.count()