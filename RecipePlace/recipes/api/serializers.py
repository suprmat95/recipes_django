from rest_framework import serializers
from ..models import Comment, Recipe, Passage, Ingredient
import locale

locale.setlocale(locale.LC_ALL, 'it_IT.UTF-8')

class PassageSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(read_only=True)
    recipe_slug = serializers.SerializerMethodField(read_only=True)
    pictures = serializers.ImageField(read_only=True)

    class Meta:
        model = Passage
        exclude = ["recipe", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d %B %Y')

    def get_recipe_slug(self, instance):
        return instance.recipe.slug

class PassagePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passage
        fields = ["pictures"]

class IngredientSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField(read_only=True)
    recipe_slug = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Ingredient
        exclude = ["recipe", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d %B %Y')

    def get_recipe_slug(self, instance):
        return instance.recipe.slug


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    user_has_voted = serializers.SerializerMethodField(read_only=True)
    recipe_slug = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        exclude = ["recipe", "voters", "updated_at"]

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d %B %Y')

    def get_likes_count(self, instance):
        return instance.voters.count()

    def get_user_has_voted(self, instance):
        request = self.context.get("request")
        return instance.voters.filter(pk=request.user.pk).exists()

    def get_recipe_slug(self, instance):
        return instance.recipe.slug

class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    created_at = serializers.SerializerMethodField(read_only=True)
    slug = serializers.SlugField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    user_has_commented = serializers.SerializerMethodField(read_only=True)
    pictures = serializers.ImageField(read_only=True)
    passage = PassageSerializer(many=True, read_only=True)
    ingredient = IngredientSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        exclude = ["updated_at"]

    def get_comments_count(self, instance):
        return instance.comments.count()

    def get_created_at(self, instance):
        return instance.created_at.strftime('%d %B %Y')

    def get_user_has_commented(self, instance):
        request = self.context.get("request")
        return instance.comments.filter(author=request.user).exists()

class RecipePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ["pictures"]


