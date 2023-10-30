from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=280)
    date_time = models.DateTimeField(auto_now_add=True)

    def formatted_date_time(self):
        return self.date_time.strftime("%m-%d-%Y %H:%M")

    def __str__(self):
        return f"{self.formatted_date_time()} {self.user} says: {self.text}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} likes: {self.post}"
