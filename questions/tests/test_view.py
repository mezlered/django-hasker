from hashlib import md5
from os import urandom
from django.test import Client, TestCase
from django.urls import reverse

from questions.models import Answer, AnswerVote, Question, QuestionVote
from .fixtures import TEST_PASSWORD, TEST_USER, CreateDataMixin


class TestAskView(CreateDataMixin, TestCase):
    def test_GET_unauthorised(self):
        client = Client()
        response = client.get(reverse("question:ask"))
        self.assertEqual(response.status_code, 302)

    def test_GET_authorised(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("question:ask"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "questions/ask.html")

    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(
            reverse("question:ask"), data={"title": "Title", "description": "Description"}
        )
        self.assertEqual(response.status_code, 302)

    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)

        before_questions_count = Question.objects.count()
        response = client.post(
            reverse("question:ask"), data={"title": "Title", "description": "Description"}
        )
        self.assertEqual(before_questions_count, Question.objects.count())


class TestQuestionDetail(CreateDataMixin, TestCase):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(
            reverse(
                "question:question", kwargs={"slug": self.question.title}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("questions/question.html")

    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(
            reverse(
                "question:question", kwargs={"slug": self.question.title}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("questions/question.html")

    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(
            reverse(
                "question:question", kwargs={"slug": self.question.title}
            ),
        )
        self.assertEqual(response.status_code, 302)

    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)

        url = reverse(
            "question:question", kwargs={"slug": self.question.title}
        )

        response = client.post(url, data={"description": "content"})
        self.assertEqual(response.status_code, 302)

        answer = Answer.objects.get(description="content")
        self.assertEqual(self.question, answer.question)


class TestQuestionSearch(CreateDataMixin, TestCase):
    def test_empty_query(self):
        client = Client()
        url = reverse("question:search")
        response = client.get(url, data={"search_": ""})
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        unique_title = md5(urandom(10)).hexdigest()
        unique_content = md5(urandom(10)).hexdigest()

        self.question.title = unique_title
        self.question.content = unique_content
        self.question.save()

        client = Client()
        url = reverse("question:search")
        response = client.get(url, data={"search_": f"{unique_title}"})
        self.assertEqual(response.status_code, 200)

    def test_query_with_tag(self):
        unique_title = md5(urandom(10)).hexdigest()
        unique_content = md5(urandom(10)).hexdigest()
        tag = "tag"

        question = Question(
            title=unique_title, description=unique_content, author=self.user
        )
        question.save()
        question.add_tags([tag])

        client = Client()
        url = reverse("question:search")

        response = client.get(url, data={"search_": f"tag:{tag}"})
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("question:tag", args=(tag,)), response.url)

        response = client.get(
            url, data={"search_": f"tag:{tag}"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
