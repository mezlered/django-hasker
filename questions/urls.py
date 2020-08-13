from django.urls import path

from .views import (
        QuestionsListView, QuestionDetailView, QuestionTopView, 
        QuestionSearch, AskView, QuestionsTag, QuestionUserView,
        approved_answer, vote_answer, vote_question 
    )


app_name = 'question'


urlpatterns = [
    path("", QuestionsListView.as_view(), name="index"),
    path("top/", QuestionTopView.as_view(), name="top_question"),
    path("question/<str:slug>/", QuestionDetailView.as_view(), name="question"),
    path("question/published/<username>/", QuestionUserView.as_view(), name="question_user"),
    path("search/", QuestionSearch.as_view(), name="search"),
    path("ask/", AskView.as_view(), name="ask"),
    path("tag/<slug>", QuestionsTag.as_view(), name="tag"),
]

# Urlpatterns AJAX
urlpatterns += [
    path("vote_answer/", vote_answer, name="vote_answer"),
    path("vote_question/", vote_question, name="vote_question"),
    path("approved_answer/<int:pk>", approved_answer, name="approved_answer"),
]