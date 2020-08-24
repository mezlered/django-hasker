
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from questions.models import Answer, Question
from questions.tests.fixtures import CreateDataMixin


class AnswersTests(CreateDataMixin, APITestCase):
    def test_answers_get(self):
        author = self.create_user()
        question = self.create_question(user=author)
        users = [self.create_user() for _ in range(5)]

        for user in users:
            self.create_answer(question, user)

        url = reverse('apiapp:api_answers', kwargs={'pk': question.pk})
        response = self.client.get(url, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 5)
        self.assertEqual(
            {item['author'] for item in data},
            {user.id for user in users},
        )

    def test_answers_post_unauthorized(self):
        author = self.create_user()
        question = self.create_question(user=author)

        url = reverse('apiapp:api_answers', kwargs={'pk': question.pk})
        response = self.client.post(
            url, data={'content': 'aaa'}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_accept_answer_unauthorized(self):
        question_author = self.create_user()
        question = self.create_question(user=question_author)
        answers = [self.create_answer(question=question) for _ in range(3)]

        url = reverse('apiapp:api_answer_details', kwargs={'pk': answers[1].pk})
        response = self.client.patch(
            url, data={'is_accepted': True}, format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
