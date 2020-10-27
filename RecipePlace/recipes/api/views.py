from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import  APIView

from ..models import Recipe, Comment, Passage, Ingredient
from ..api.serializers import RecipeSerializer, RecipePictureSerializer\
    , CommentSerializer, PassageSerializer, IngredientSerializer
from ..api.permission import IsAuthorOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by("-created_at")
    lookup_field = "slug"
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        recipe = get_object_or_404(Recipe, slug = kwarg_slug)

        if recipe.comments.filter(author=request_user).exists():
            raise ValidationError("Hai già risposto a questa domanda")

        serializer.save(author=request_user, recipe=recipe)

class PassageCreateAPIView(generics.CreateAPIView):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        recipe = get_object_or_404(Recipe, slug = kwarg_slug)
        serializer.save(recipe=recipe)

class IngredientCreateAPIView(generics.CreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        recipe = get_object_or_404(Recipe, slug = kwarg_slug)
        serializer.save(recipe=recipe)

class RecipeIngredientListAPIView(generics.ListAPIView):
    serializer_class = IngredientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Ingredient.objects.filter(recipe__slug=kwarg_slug).order_by("-created_at")



class RecipeCommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Comment.objects.filter(recipe__slug=kwarg_slug).order_by("-created_at")

class RecipePassageListAPIView(generics.ListAPIView):
    serializer_class = PassageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Passage.objects.filter(recipe__slug=kwarg_slug).order_by("-created_at")


class CommentLikeAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user

        comment.voters.remove(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        user = self.request.user

        comment.voters.add(user)
        comment.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(comment, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)


class PictureUpdateView(generics.UpdateAPIView):
    serializer_class = RecipePictureSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        recipe_object = self.request.question
        return recipe_object



class CommentRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class PassageRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]