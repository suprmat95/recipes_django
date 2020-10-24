from django.shortcuts import get_object_or_404

from rest_framework import viewsets, generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import  APIView

from ..models import Question, Answer, Passage
from ..api.serializers import QuestionSerializer, QuestionPictureSerializer\
    , AnswerSerializer, PassageSerializer
from ..api.permission import IsAuthorOrReadOnly

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by("-created_at")
    lookup_field = "slug"
    serializer_class = QuestionSerializer
    permission_classes = [IsAuthorOrReadOnly, IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class AnswerCreateAPIView(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug = kwarg_slug)

        if question.answers.filter(author=request_user).exists():
            raise ValidationError("Hai già risposto a questa domanda")

        serializer.save(author=request_user, question=question)

class PassageCreateAPIView(generics.CreateAPIView):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request_user = self.request.user
        kwarg_slug = self.kwargs.get("slug")
        question = get_object_or_404(Question, slug = kwarg_slug)
        serializer.save(question=question)

class QuestionAnswerListAPIView(generics.ListAPIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Answer.objects.filter(question__slug=kwarg_slug).order_by("-created_at")

class QuestionPassageListAPIView(generics.ListAPIView):
    serializer_class = PassageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        kwarg_slug = self.kwargs.get("slug")
        return Passage.objects.filter(question__slug=kwarg_slug).order_by("-created_at")

class AnswerLikeAPIView(APIView):
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = self.request.user

        answer.voters.remove(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        answer = get_object_or_404(Answer, pk=pk)
        user = self.request.user

        answer.voters.add(user)
        answer.save()

        serializer_context = {"request": request}
        serializer = self.serializer_class(answer, context=serializer_context)

        return Response(serializer.data, status=status.HTTP_200_OK)

class PictureUpdateView(generics.UpdateAPIView):
    serializer_class = QuestionPictureSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        question_object = self.request.question
        return question_object


class AnswerRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

class PassageRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Passage.objects.all()
    serializer_class = PassageSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]