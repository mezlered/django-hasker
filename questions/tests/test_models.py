from django.test import TestCase
from questions.models import VOTE_DOWN, VOTE_UP, Answer, AnswerVote, Question

from .fixtures import CreateDataMixin


class TestAnswer(CreateDataMixin, TestCase):
    def test_accepted(self):
        self.answer_1.accepted()
        self.assertTrue(self.answer_1.is_accepted)
        self.assertFalse(self.answer_2.is_accepted)

        self.answer_2.accepted()
        self.answer_1.refresh_from_db()
        self.assertTrue(self.answer_2.is_accepted)
        self.assertFalse(self.answer_1.is_accepted)

    def test_unaccepted(self):
        self.answer_1.accepted()
        self.answer_2.refresh_from_db()
        self.assertTrue(self.answer_1.is_accepted)
        self.assertFalse(self.answer_2.is_accepted)

        self.answer_1.unaccepted()
        self.answer_2.refresh_from_db()
        self.assertFalse(self.answer_1.is_accepted)
        self.assertFalse(self.answer_2.is_accepted)


class TestAnswerVote(CreateDataMixin, TestCase):
    def test_answer_vote(self):
        rating_0 = self.answer_1.change_vote(self.user, VOTE_UP)
        self.assertEqual(rating_0, self.answer_1.rating)

        rating_1 = self.answer_1.change_vote(self.user, VOTE_UP)
        self.assertEqual(rating_1, self.answer_1.rating)
        self.assertEqual(rating_1, rating_0)

        rating_2 = self.answer_1.change_vote(self.user, VOTE_DOWN)
        self.answer_1.refresh_from_db()
        self.assertEqual(rating_2, self.answer_1.rating)
        self.assertEqual(rating_2, rating_1 - 1)
        self.assertFalse(AnswerVote.objects.exists())


class TestQuestion(CreateDataMixin, TestCase):
    def test_trending(self):
        users = [
            self.user_model(username="user1", email="user1@mail.fake"),
            self.user_model(username="user2", email="user2@mail.fake"),
            self.user_model(username="user3", email="user3@mail.fake"),
        ]

        for user in users:
            user.save()

        questions = [
            Question(author=users[0], title="A0", description="B0"),
            Question(author=users[1], title="A1", description="B1"),
            Question(author=users[2], title="A2", description="B2"),
        ]

        for question in questions:
            question.save()

        questions[0].change_vote(users[0], VOTE_UP)
        questions[0].change_vote(users[1], VOTE_UP)
        questions[0].change_vote(users[2], VOTE_UP)

        questions[1].change_vote(users[0], VOTE_UP)
        questions[1].change_vote(users[1], VOTE_UP)

        questions[2].change_vote(users[0], VOTE_UP)
        questions[2].change_vote(users[1], VOTE_UP)
        questions[2].change_vote(users[2], VOTE_DOWN)

       
        for question in questions:
            question.save()

        trending_questions = list(Question.trending(3))
        self.assertEqual(3, len(trending_questions))
        self.assertEqual(questions[0].pk, trending_questions[0].pk)
        self.assertEqual(questions[1].pk, trending_questions[1].pk)
        self.assertEqual(questions[2].pk, trending_questions[2].pk)


    def test_add_tags(self):
        question = Question(author=self.user, title="A", description="B")

        with self.assertRaises(ValueError):
            question.add_tags(["tag1", "tag2"])

        question.save()
        tags = ["tag1", "tag2", "tag3"]
        question.add_tags(tags)

        self.assertEqual(
            set(tags), set(question.tags.values_list("name", flat=True))
        )


class TestQuestionVote(CreateDataMixin, TestCase):
    def test_question_vote(self):
        rating_0 = self.question.change_vote(self.user, VOTE_UP)
        self.question.save()
        self.question.refresh_from_db()
        self.assertEqual(rating_0, self.question.rating)

        rating_1 = self.question.change_vote(self.user, VOTE_UP)
        self.question.save()
        self.question.refresh_from_db()
        self.assertEqual(rating_1, self.question.rating)
        self.assertEqual(rating_1, rating_0)

        rating_2 = self.question.change_vote(self.user, VOTE_DOWN)
        self.question.save()
        self.question.refresh_from_db()
        self.assertEqual(rating_2, self.question.rating)
        self.assertEqual(rating_2, rating_1 - 1)

        rating_3 = self.question.change_vote(self.user, VOTE_DOWN)
        self.question.save()
        self.question.refresh_from_db()
        self.assertEqual(rating_3, self.question.rating)
        self.assertEqual(rating_3, rating_2 - 1)

        rating_4 = self.question.change_vote(self.user, VOTE_UP)
        self.question.save()
        self.question.refresh_from_db()
        self.assertEqual(rating_4, self.question.rating)
        self.assertEqual(rating_4, 0)
