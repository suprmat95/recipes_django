from django.urls import include, path
from rest_framework.routers import DefaultRouter
from ..api import views as qv

router = DefaultRouter()
router.register(r"questions", qv.QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),

    path("questions/<slug:slug>/answers/",
         qv.QuestionAnswerListAPIView.as_view(),
         name="question-answers-list"),

    path("questions/<slug:slug>/answer/",
         qv.AnswerCreateAPIView.as_view(),
         name="create-answer"),

    path("questions/<slug:slug>/passages/",
         qv.QuestionPassageListAPIView.as_view(),
         name="question-passage-list"),

    path("questions/<slug:slug>/passage/",
         qv.PassageCreateAPIView.as_view(),
         name="create-passage"),

    path("questions/<slug:slug>/ingredients/",
         qv.QuestionIngredientListAPIView.as_view(),
         name="question-ingredients-list"),

    path("questions/<slug:slug>/ingredient/",
         qv.IngredientCreateAPIView.as_view(),
         name="create-ingredient"),

    path("answers/<int:pk>/",
         qv.AnswerRUDAPIView.as_view(),
         name="answer-detail"),

    path("answers/<int:pk>/like/",
         qv.AnswerLikeAPIView.as_view(),
         name="answer-like"),
    path("picture/", qv.PictureUpdateView.as_view(), name="picture-update")

]