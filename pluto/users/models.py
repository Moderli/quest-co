# models.py
from django.db import models
from django.contrib.auth.models import User


class Interest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(default=False)
    user_name = models.CharField(max_length=50, blank=True, null=True)
    tags = models.ManyToManyField(Interest, blank=True)
    question_text = models.CharField(max_length=255)
    question_description = models.TextField(blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.question_text

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True, null=True)
    description = models.TextField(blank=True)
    interests = models.ManyToManyField(Interest, blank=True)

    def __str__(self):
        return self.user.username

from django.db import models
from django.contrib.auth.models import User

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    answer_text = models.TextField()
    answer_id = models.CharField(max_length=50)  # You can adjust the max_length as needed

    def __str__(self):
        return f"Answer by {self.user.username} to {self.question.question_text}"



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.question.question_text}"
