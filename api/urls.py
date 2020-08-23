from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from config.base import API_VERSION

from .views import (AnswerDetailsAPIView, AnswersAPIView, AnswerVotesAPIView,
                    QuestionAPIView, QuestionDetailsAPIView,
                    QuestionVotesAPIView)

app_name = 'apiapp'

urlpatterns = [
    path(f'{API_VERSION}/token', obtain_auth_token, name='api_obtain_token'),
    path(f'{API_VERSION}/questions/', QuestionAPIView.as_view(), name='api_questions'),
    path(f'{API_VERSION}/questions/<int:pk>/', QuestionDetailsAPIView.as_view(), name='api_question_details'),
    path(f'{API_VERSION}/questions/<int:pk>/answers', AnswersAPIView.as_view(), name='api_answers'),
    path(f'{API_VERSION}/questions/<int:pk>/votes', QuestionVotesAPIView.as_view(), name='api_question_votes'),
    path(f'{API_VERSION}/answers/<int:pk>', AnswerDetailsAPIView.as_view(), name='api_answer_details'),
    path(f'{API_VERSION}answers/<int:pk>/votes', AnswerVotesAPIView.as_view(), name='api_answer_votes'),
 ]
