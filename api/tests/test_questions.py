from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from questions.tests.fixtures import CreateDataMixin
from questions.models import Question


class QuestionsTests(CreateDataMixin, APITestCase):
    def test_questions_get(self):
        user = self.create_user()

        for _ in range(5):
            self.create_question(user)

        url = reverse('apiapp:api_questions')
        response = self.client.get(url, format='json')
        data = response.json()

        count = Question.objects.count()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), count)


    def test_questions_get_search(self):
        user = self.create_user()
        questions = [self.create_question(user) for _ in range(5)]

        q = questions[2].title[:5]
        url = reverse('apiapp:api_questions')

        response = self.client.get(url + f'?search={q}', format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], questions[2].id)


    def test_questions_post_unauthorized(self):
        url = reverse('apiapp:api_questions')
        response = self.client.post(
            url,
            data={'description': 'aaa', 'title': 'aaa', 'tags': ['tag1', 'tag2']},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_question_details(self):
        user = self.create_user()
        question = self.create_question(user)

        url = reverse('apiapp:api_question_details', kwargs={'pk': question.pk})
        response = self.client.get(url, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('author'), user.id)
        self.assertEqual(data.get('description'), question.description)
        self.assertEqual(data.get('title'), question.title)


    def test_question_votes_get(self):
        user = self.create_user()
        question = self.create_question(user)

        voters = [self.create_user() for _ in range(3)]
        for voter, value in zip(voters, [1, -1, 1]):
            question.change_vote(voter, value)

        url = reverse('apiapp:api_question_votes', kwargs={'pk': question.pk})
        response = self.client.get(url, format='json')
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 3)
        self.assertEqual(
            sum(item['value_vote'] for item in data), 1
        )

    def test_question_votes_post_unauthorized(self):
        user = self.create_user()
        question = self.create_question(user)

        url = reverse('apiapp:api_question_votes', kwargs={'pk': question.pk})
        response = self.client.post(url, data={'value': 1}, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


