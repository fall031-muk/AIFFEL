import json

from django.test import TestCase, Client

from .models import User


class SignUpTest(TestCase):
    def test_signup_success(self):
        client = Client()
        user = {
            "user_id": "muk",
            "password": "muk1234",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    user_id="muk2",
                    password="muk1234"
                ),
                User(
                    id=2,
                    user_id="muk3",
                    password="muk1234"
                )
            ]
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_duplication(self):
        client = Client()
        user = {
            "user_id": "muk2",
            "password": "muk123",
        }
        response = client.post(
            "/users/signup", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "DUPLICATION_ERROR"})

class SigninTest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    user_id="muk",
                    password="$2b$12$sk3uJkzhQz8H9xAiWtU.OOAoKORrsZvJywCkinKr9JR.mf7Jyueuq", #"muk1234"의 암호화된 password
                ),

            ]
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_login_success(self):
        user = {
            "user_id": "muk",
            "password": "muk1234",
        }
        client = Client()

        response = client.post(
            "/users/signin", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        
    def test_signinview_not_exist_user(self):
        client = Client()
        user = {
            "user_id" : "muk2",
            "password": "muk12345",
        }
        response = client.post(
            "/users/signin", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "USER_DOES_NOT_EXIST"})

    def test_signinview_invalid_password(self):
        client = Client()
        user = {
            "user_id" : "muk",
            "password": "muk123456",
        }
        response = client.post(
            "/users/signin", json.dumps(user), content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "INVALID_PASSWORD"})