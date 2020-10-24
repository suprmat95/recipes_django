from django.db import models
from django.conf import settings
class Question(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=240)
    slug = models.SlugField(max_length=255, unique=True)
    picture = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="questions")

    def __str__(self):
        return self.content

class Answer(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name="answers")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="votes")

class Passage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name="passage")
    picture = models.ImageField(null=True, blank=True)

class Ingredient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name="ingredient")
    quantity = models.IntegerField(null=True, blank=True)
    unity = models.TextField()
