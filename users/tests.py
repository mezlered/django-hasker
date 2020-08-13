from django.contrib.auth import get_user_model

from django.test import TestCase, Client
from django.urls import reverse


TEST_USER = "test_user"
TEST_PASSWORD = "test_password_123"


class CreateDataMixin:
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_model = get_user_model()

        cls.user = cls.user_model(
            username=TEST_USER, email="test_user@mail.fake"
        )
        cls.user.set_password(TEST_PASSWORD)
        cls.user.save()


class TestLogIn(CreateDataMixin, TestCase):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(reverse("users:login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("users/login.html")


    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("question:index"))

        self.assertEqual(response.status_code, 200)


    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(reverse("users:login"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("question:index"), response.url)

        response = client.post(reverse("users:login"), follow=True)

        self.assertRedirects(response, reverse("users:settings"))


    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(
            reverse("users:login"),
            data={"username": TEST_USER, "password": TEST_PASSWORD},
            follow=True,
        )

        self.assertRedirects(response, reverse("question:index"))


class TestLogOut(CreateDataMixin, TestCase):
    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(reverse("users:logout"), data={}, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("question:index"))


    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(reverse("users:logout"), data={}, follow=True)
        self.assertEqual(response.status_code, 200)


class TestSignUp(CreateDataMixin, TestCase):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(reverse("users:signup"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("users/registrations.html")

    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("users:signup"), follow=True)

        self.assertRedirects(response, reverse("question:index"))


    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(reverse("users:signup"), follow=True)

        self.assertRedirects(response, reverse("question:index"))


    def test_POST_registration(self):
        client = Client()
        response = client.post(
            reverse("users:signup"),
            data={
                "username": "new_user",
                "email": "new_user_email@mail.fake",
                "password1": "new_password_123",
                "password2": "new_password_123",
            },
            follow=True,
        )
        self.assertRedirects(response, reverse("users:settings"))
        self.assertTrue(
            self.user_model.objects.filter(username="new_user").exists()
        )


class TestSettings(CreateDataMixin, TestCase):
    def test_GET_unauthorized(self):
        client = Client()
        response = client.get(reverse("users:settings"))
        self.assertRedirects(response, reverse("users:login"))


    def test_GET_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.get(reverse("users:settings"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("users/settings.html")


    def test_POST_unauthorized(self):
        client = Client()
        response = client.post(
            reverse("users:settings"), data={"email": "some_new_email@mail.fake"}
        )
        self.assertRedirects(response, reverse("users:login"))


    def test_POST_authorized(self):
        client = Client()
        client.login(username=TEST_USER, password=TEST_PASSWORD)
        response = client.post(
            reverse("users:settings"),
            data={"email": "some_new_email@mail.fake"},
            follow=True,
        )
        self.assertRedirects(response, reverse("users:settings"))
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "some_new_email@mail.fake")
