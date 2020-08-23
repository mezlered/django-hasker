from rest_framework import filters
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     get_object_or_404)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from questions.models import Answer, AnswerVote, Question, QuestionVote
from users.models import User

from .permissions import IsOwnerOfQuestionOrReadOnly
from .serializers import (AnswerDetailSerializer, AnswerSerializer,
                          AnswerVoteSerializer, QuestionSerialiser,
                          QuestionVoteSerializer)


class QuestionAPIView(ListCreateAPIView):
    filter_backends = [filters.SearchFilter,]
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['title', 'description']

    queryset = Question.objects.all()
    serializer_class = QuestionSerialiser

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data.get('author'))
        return serializer.save(author=author)

    def get_queryset(self):
        queryset = Question.objects.all()
        queryset = queryset.select_related('author')
        queryset = queryset.prefetch_related('tags')
        return queryset


class QuestionDetailsAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Question.objects.all()
    serializer_class = QuestionSerialiser

    def get_queryset(self):
        queryset = Question.objects.all()
        queryset = queryset.select_related('author')
        queryset = queryset.prefetch_related('tags')

        return queryset

class QuestionVotesAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = QuestionVoteSerializer

    def initial(self, request, *args, **kwargs):
        '''
        Runs anything that needs to occur prior to calling the method handler.
        '''
        super().initial(request, *args, **kwargs)
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        queryset = QuestionVote.objects.all()
        queryset = queryset.select_related('author')
        queryset = queryset.filter(to=self.question)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, to=self.question)


class AnswersAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AnswerSerializer

    def initial(self, request, *args, **kwargs):
        '''
        Runs anything that needs to occur prior to calling the method handler.
        '''
        super().initial(request, *args, **kwargs)
        self.question = get_object_or_404(Question, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        queryset = Answer.objects.all()
        queryset = queryset.filter(question=self.question)
        queryset = queryset.order_by('-is_accepted', '-rating', '-date_publication')
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, question=self.question)


class AnswerDetailsAPIView(RetrieveUpdateAPIView):
    http_method_names = ['get', 'patch', 'head', 'options']
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsOwnerOfQuestionOrReadOnly,
    ]
    serializer_class = AnswerDetailSerializer

    def get_queryset(self):
        queryset = Answer.objects.all()
        queryset = queryset.select_related('author')

        return queryset


class AnswerVotesAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = AnswerVoteSerializer

    def initial(self, request, *args, **kwargs):
        '''
        Runs anything that needs to occur prior to calling the method handler.
        '''
        super().initial(request, *args, **kwargs)
        self.answer = get_object_or_404(Answer, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        queryset = AnswerVote.objects.all()
        queryset = queryset.select_related('author')
        queryset = queryset.filter(to=self.answer)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, to=self.answer)
