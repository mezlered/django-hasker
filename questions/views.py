from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden, JsonResponse, request
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.list import ListView

from config.base import PAGITATE_BY
from users.mixins import UserRequired

from .forms import AnswerForm, AskForm, SearchForm, VoteForm
from .mixins import TredingMixin
from .models import Answer, Question


class QuestionsListView(TredingMixin, ListView):
    """ List of all questions sorted default: -date_publication."""

    model = Question
    template_name = "questions/index.html"
    paginate_by = PAGITATE_BY

    def get_queryset(self):
        queryset = Question.hewy.all()
        return queryset.select_related("author").prefetch_related("tags")


class QuestionTopView(QuestionsListView):
    """ List of all questions sorted rating."""

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by("-rating",)


class QuestionUserView(QuestionsListView):
    """ List of questions current user."""

    ordering = ("-rating",)

    def get_queryset(self):
        queryset = super().get_queryset()
        username = self.kwargs["username"]
        return queryset.filter(author__username=username)


class QuestionsTag(QuestionsListView):
    """ List of questions current tag."""
    
    ordering = ("-rating",)

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.kwargs["slug"].strip().lower()
        return queryset.filter(tags__name=tag)


class QuestionDetailView(TredingMixin, ListView):
    """ Question details / list answer. """

    form = None
    model = Answer
    ordering = ("date_publication", "-rating",)
    template_name = "questions/question.html"
    paginate_by = PAGITATE_BY
    login_url = reverse_lazy("users:login")


    def dispatch(self, *args, **kwargs):
        self.question = get_object_or_404(Question, title=self.kwargs["slug"])
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(question=self.question)
        self.answers_count = queryset.count()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["question"] = self.question
        context["answers_count"] = self.answers_count
        return context

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect("users:login")
        
        form = AnswerForm(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    @transaction.atomic
    def form_valid(self, form):
        answer = form.save(commit=False)
        answer.author = self.request.user
        answer.question = self.question
        answer.save()
        return redirect(self.request.build_absolute_uri())

    def form_invalid(self, form):
        self.rorm = form
        return super().get(self.request)


class QuestionSearch(QuestionsListView):
    """
    Search by title and description of questions.
    Search for tag related questions
    """

    search = ""
    def get(self, *args, **kwargs):
        self.search = self.request.GET.get("search_")

        if self.search.startswith("tag:"):                #search tag
            _, tag = self.search.split("tag:")
            tag = tag.lower().strip()
            return redirect("question:tag", slug=tag)
        return super().get(*args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            queryset = queryset.filter(
                Q(title__icontains=self.search) | Q(description__icontains=self.search)
            )
        return queryset


class AskView(TredingMixin, LoginRequiredMixin, CreateView):
    """ View add answer. """

    form_class = AskForm
    model = Question
    template_name = "questions/ask.html"
    success_url = reverse_lazy("question:index")
    login_url = reverse_lazy("users:login")

    @transaction.atomic
    def form_valid(self, form):
        question = form.save(commit=False)
        question.author = self.request.user
        question.save()

        tags = form.cleaned_data["tags"]
        question.add_tags(tags)

        return redirect(self.success_url)


def vote_answer(request):
    """Vote for a answer. Only AJAX request by post method."""

    form = VoteForm(request.POST)
    if form.is_valid() and request.is_ajax():
        target = form.cleaned_data["target_id"]
        value = form.cleaned_data["value"]

        pub = Question.objects.get(id=target)
        rating = pub.change_vote(value=value, user=request.user)
        pub.rating = rating
        pub.vlue_vote = value
        pub.save()
        return JsonResponse(data={"rating": rating})

    return JsonResponse(data=form.errors, status=400)


def vote_question(request):
    """Vote for a question. Only AJAX request by post method."""

    form = VoteForm(request.POST)
    if form.is_valid() and request.is_ajax():
        if not request.user.is_authenticated:

            return HttpResponseForbidden()

        target = form.cleaned_data["target_id"]
        value = form.cleaned_data["value"]

        pub = Answer.objects.get(id=target)
        rating = pub.change_vote(value=value, user=request.user)
        pub.rating = rating
        pub.vlue_vote = value
        pub.save()
        return JsonResponse(data={"rating": rating})

    return JsonResponse(data=form.errors, status=400)


def approved_answer(request, pk):
    """Approved answer. Only AJAX request by post method."""
    
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    if request.method == "POST" and request.is_ajax():
        answer = Answer.objects.get(id=pk)

        if answer.question.author != request.user:
            return HttpResponseForbidden()

        if answer.is_accepted:
            answer.unaccepted()
        else:
            answer.accepted()

        return JsonResponse(data={"is_accepted": answer.is_accepted})
