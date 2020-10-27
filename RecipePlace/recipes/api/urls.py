from django.conf.urls import url
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView

from ..api import views as qv

router = DefaultRouter()
router.register(r"recipes", qv.RecipeViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("recipes/<slug:slug>/comments/",
         qv.RecipeCommentListAPIView.as_view(),
         name="recipe-comments-list"),

    path("recipes/<slug:slug>/comment/",
         qv.CommentCreateAPIView.as_view(),
         name="create-comment"),

    path("recipes/<slug:slug>/passages/",
         qv.RecipePassageListAPIView.as_view(),
         name="recipe-passage-list"),

    path("recipes/<slug:slug>/passage/",
         qv.PassageCreateAPIView.as_view(),
         name="create-passage"),

    path("recipes/<slug:slug>/ingredients/",
         qv.RecipeIngredientListAPIView.as_view(),
         name="recipe-ingredients-list"),

    path("recipes/<slug:slug>/ingredient/",
         qv.IngredientCreateAPIView.as_view(),
         name="create-ingredient"),

    path("comment/<int:pk>/",
         qv.CommentRUDAPIView.as_view(),
         name="comment-detail"),

    path("comments/<int:pk>/like/",
         qv.CommentLikeAPIView.as_view(),
         name="comment-like"),

    path("picture/", qv.PictureUpdateView.as_view(), name="picture-update"),


]