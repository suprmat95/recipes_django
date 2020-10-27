from django.db import models
from django.conf import settings

"""
Model of Recipes
"""
class Recipe(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=240)
    description = models.CharField(max_length=1000)
    time_to_prepare = models.CharField(max_length=10)
    people = models.CharField(max_length=10)
    slug = models.SlugField(max_length=255, unique=True)
    picture = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="recipes")

    def __str__(self):
        return self.content

"""
Model for Comments of Recipes
"""
class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    recipe = models.ForeignKey(Recipe,
                                 on_delete=models.CASCADE,
                                 related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE)
    voters = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                    related_name="votes")

    def __str__(self):
        return self.author.username

"""
Model for Passages of Recipes
"""
class Passage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    picture = models.ImageField(null=True, blank=True)
    recipe = models.ForeignKey(Recipe,
                                 on_delete=models.CASCADE,
                                 related_name="passage")

"""
Model for Ingredients of Recipes
"""
class Ingredient(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    name = models.TextField()
    quantity = models.TextField()
    unity = models.TextField()
    recipe = models.ForeignKey(Recipe,
                                 on_delete=models.CASCADE,
                                 related_name="ingredient")

