import json, jwt, datetime

from django.test import TestCase, Client

from questions.models import Question, Like, Comment
from users.models import User

from config.settings import SECRET_KEY


class QuestionViewtest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    user_id="muk",
                    password="muk1234"
                ),
                User(
                    id=2,
                    user_id="muk2",
                    password="muk12345"
                )
            ]
        )
        self.time = datetime.datetime.now().strftime('%Y-%m-%d')
        Question.objects.bulk_create(
            [
                Question(
                    id=1,
                    user_id=User.objects.get(id=1).id,
                    title="1번 질문", 
                    like_count = 0,
                    content="1번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=2,
                    user_id=User.objects.get(id=1).id,
                    title="2번 질문", 
                    like_count = 10,
                    content="2번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=3,
                    user_id=User.objects.get(id=1).id,
                    title="3번 질문", 
                    like_count = 0,
                    content="3번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=4,
                    user_id=User.objects.get(id=2).id,
                    title="4번 질문", 
                    like_count = 0,
                    content="4번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=5,
                    user_id=User.objects.get(id=2).id,
                    title="5번 질문", 
                    like_count = 0,
                    content="5번 질문 내용입니다",
                    # created_at = self.time
                ),            
            ]
        )
    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()

    def test_create_question_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        question = {
               
            "user_id"    :User.objects.get(id=1).id,
            "title"      :"6번 질문", 
            "like_count" : 0,
            "content"    :"6번 질문 내용입니다",
            "created_at" : self.time
        }
        response = client.post(
            "/questions", json.dumps(question), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "CREATE", 
        "data": {
            "title"     : "6번 질문",
            "content"   : "6번 질문 내용입니다",
            "user"      : "muk",
            "created_at": self.time
            }
        }
        )
    def test_create_key_error(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        question = {
            "user_id"    :User.objects.get(id=1).id,
            "titleeeee"  :"7번 질문", 
            "like_count" : 0,
            "content"    :"7번 질문 내용입니다",
            "created_at" : self.time
        }
        response = client.post(
            "/questions", json.dumps(question), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})

    def test_question_edit_success(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        question = {
            "title"   : "수정 질문",
            "content" : "수정 내용입니다",
        }
        response = client.put(
            "/questions/1", json.dumps(question), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "SUCCESS"})

    def test_edit_not_matched_user(self):
        access_token = jwt.encode({"id": 2}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        question = {
            "title"   : "수정 질문",
            "content" : "수정 내용입니다",
        }
        response = client.put(
            "/questions/1", json.dumps(question), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "NOT_MATCHED_USER"})

    def test_question_does_not_exist(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        question = {
            "title"   : "수정 질문",
            "content" : "수정 내용입니다",
        }
        response = client.put(
            "/questions/100", json.dumps(question), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "QUESTION_DOES_NOT_EXIST"})

    def test_question_edit_key_error(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        question = {
            "titleee" : "수정 질문",
            "content" : "수정 내용입니다",
        }
        response = client.put(
            "/questions/1", json.dumps(question), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR"})

    def test_question_delete_success(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/questions/1", **header)

        self.assertEqual(response.status_code, 204)

    def test_question_delete_not_authorization_user(self):
        access_token = jwt.encode({"id": 2}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/questions/1", **header)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE": "NOT_MATCHED_USER"})

    def test_question_delete_does_not_exist(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm='HS256')
        client = Client()

        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.delete("/questions/100", **header)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "QUESTION_DOES_NOT_EXIST"})

class CommentViewtest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    user_id="muk",
                    password="muk1234"
                ),
                User(
                    id=2,
                    user_id="muk2",
                    password="muk12345"
                )
            ]
        )
        self.time = datetime.datetime.now().strftime('%Y-%m-%d')
        Question.objects.bulk_create(
            [
                Question(
                    id=1,
                    user_id=User.objects.get(id=1).id,
                    title="1번 질문", 
                    like_count = 0,
                    content="1번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=2,
                    user_id=User.objects.get(id=1).id,
                    title="2번 질문", 
                    like_count = 10,
                    content="2번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=3,
                    user_id=User.objects.get(id=1).id,
                    title="3번 질문", 
                    like_count = 0,
                    content="3번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=4,
                    user_id=User.objects.get(id=2).id,
                    title="4번 질문", 
                    like_count = 0,
                    content="4번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=5,
                    user_id=User.objects.get(id=2).id,
                    title="5번 질문", 
                    like_count = 0,
                    content="5번 질문 내용입니다",
                    created_at = self.time
                ),            
            ]
        )
        Comment.objects.bulk_create(
            [
                Comment(
                    id=1,
                    user_id=User.objects.get(id=1).id,
                    question_id=Question.objects.get(id=1).id,
                    content="1번 질문의 댓글",
                ),
                Comment(
                    id=2,
                    user_id=User.objects.get(id=1).id,
                    question_id=Question.objects.get(id=2).id,
                    content="2번 질문의 댓글",
                ),
                Comment(
                    id=3,
                    user_id=User.objects.get(id=1).id,
                    question_id=Question.objects.get(id=1).id,
                    content="1번 질문의 댓글(2)",
                ),
            ]
        )

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()
        Comment.objects.all().delete()

    def test_create_comment_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        comment = {
            "user_id"     :User.objects.get(id=1).id,
            "question_id" :Question.objects.get(id=1).id,
            "content"     :"댓글(1)",
        }
        response = client.post(
            "/questions/1/comments", json.dumps(comment), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "CREATE" }
        )

    def test_create_comment_key_error(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        comment = {
            "user_id"     :User.objects.get(id=1).id,
            "question_id" :Question.objects.get(id=1).id,
            "contenttttt" :"댓글(1)",
        }
        response = client.post(
            "/questions/1/comments", json.dumps(comment), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY_ERROR" }
        )

    def test_create_comment_empty_content(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        comment = {
            "user_id"     :User.objects.get(id=1).id,
            "question_id" :Question.objects.get(id=1).id,
            "content"     :"",
        }
        response = client.post(
            "/questions/1/comments", json.dumps(comment), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "EMPTY_CONTENT" }
        )

    def test_get_comment_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.get(
            "/questions/1/comments", **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                "Title": "1번 질문" ,
                "Result": [
                    {
                        "content" : "1번 질문의 댓글"
                    },
                    {
                        "content" : "1번 질문의 댓글(2)"
                    }
                ]             
            }
        )

class QuestionSearchViewtest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    user_id="muk",
                    password="muk1234"
                ),
                User(
                    id=2,
                    user_id="muk2",
                    password="muk12345"
                )
            ]
        )
        self.time = datetime.datetime.now().strftime('%Y-%m-%d')
        Question.objects.bulk_create(
            [
                Question(
                    id=1,
                    user_id=User.objects.get(id=1).id,
                    title="1번 질문", 
                    like_count = 0,
                    content="1번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=2,
                    user_id=User.objects.get(id=1).id,
                    title="2번 질문", 
                    like_count = 10,
                    content="2번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=3,
                    user_id=User.objects.get(id=1).id,
                    title="3번 질문", 
                    like_count = 0,
                    content="3번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=4,
                    user_id=User.objects.get(id=2).id,
                    title="4번 질문", 
                    like_count = 0,
                    content="4번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=5,
                    user_id=User.objects.get(id=2).id,
                    title="5번 질문", 
                    like_count = 0,
                    content="5번 질문 내용입니다",
                    created_at = self.time
                ),            
            ]
        )

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()

    def test_get_question_search_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.get(
            "/questions/list?title=1번", **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                "Result": [
                    {
                        "title"      : "1번 질문",
                        "content"    : "1번 질문 내용입니다",
                        "user"       : "muk",
                        "created_at" : self.time
                    },
                ]             
            }
        )

class LikeViewtest(TestCase):
    def setUp(self):
        User.objects.bulk_create(
            [
                User(
                    id=1,
                    user_id="muk",
                    password="muk1234"
                ),
                User(
                    id=2,
                    user_id="muk2",
                    password="muk12345"
                )
            ]
        )
        self.time = datetime.datetime.now().strftime('%Y-%m-%d')
        Question.objects.bulk_create(
            [
                Question(
                    id=1,
                    user_id=User.objects.get(id=1).id,
                    title="1번 질문", 
                    like_count = 1,
                    content="1번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=2,
                    user_id=User.objects.get(id=1).id,
                    title="2번 질문", 
                    like_count = 10,
                    content="2번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=3,
                    user_id=User.objects.get(id=1).id,
                    title="3번 질문", 
                    like_count = 0,
                    content="3번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=4,
                    user_id=User.objects.get(id=2).id,
                    title="4번 질문", 
                    like_count = 0,
                    content="4번 질문 내용입니다",
                    created_at = self.time
                ),
                Question(
                    id=5,
                    user_id=User.objects.get(id=2).id,
                    title="5번 질문", 
                    like_count = 0,
                    content="5번 질문 내용입니다",
                    created_at = self.time
                ),            
            ]
        )
        Like.objects.bulk_create(
            [
                    Like(
                    id=1,
                    user_id=User.objects.get(id=1).id,
                    question_id=Question.objects.get(id=1).id
                ),
            ]
        )

    def tearDown(self):
        Question.objects.all().delete()
        User.objects.all().delete()

    def test_like_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        like = {
            "question_id" :Question.objects.get(id=2).id
       }
        response = client.post(
            "/questions/like", json.dumps(like), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "LIKE" }
        )

    def test_like_cancel_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        like = {
            "question_id" :Question.objects.get(id=1).id
       }
        response = client.post(
            "/questions/like", json.dumps(like), **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE": "LIKE_CANCEL" }
        )

    def test_like_key_error(self):
        access_token = jwt.encode({"id": 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        like = {
            "question_iddd" :Question.objects.get(id=1).id
       }
        response = client.post("/questions/like", json.dumps(like), **header, content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE": "KEY ERROR"})

    def test_get_monthly_most_like_question_success(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.get(
            "/questions/like?year=2021&month=12", **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                "Result": [
                    {
                        "title"      : "2번 질문",
                        "content"    : "2번 질문 내용입니다",
                        "user"       : "muk",
                        "like_count" : 10,
                        "created_at" : self.time
                    },
                ]             
            }
        )

    def test_get_monthly_most_like_question_does_not_exist(self):
        access_token = jwt.encode({'id': 1}, SECRET_KEY, algorithm='HS256')
        client = Client()
        header = {"HTTP_AUTHORIZATION": access_token}
        response = client.get(
            "/questions/like?year=2021&month=11", **header, content_type="application/json"
        )

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"MESSAGE": "QUESTION_DOES_NOT_EXIST"})