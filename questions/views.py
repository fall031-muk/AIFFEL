import json

from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Max 

from .models import Question, Comment, Like
from users.signin_decorator import signin_decorator

class QuestionView(View):
    @signin_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            title   = data['title']
            content = data['content']

            question = Question.objects.create(
                title   = title,
                content = content,
                user    = user
            )

            Result = {
                "title"      : question.title,
                "content"    : question.content,
                "user"       : question.user.user_id,
                "created_at" : question.created_at.strftime('%Y-%m-%d')
            }

            return JsonResponse({"MESSAGE":"CREATE", "data":Result}, status=201)
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    @signin_decorator
    def put(self, request, question_id):
        try:
            if not request.user == Question.objects.get(id=question_id).user:
                return JsonResponse({"MESSAGE":"NOT_MATCHED_USER"}, status=401)

            data     = json.loads(request.body)
            title    = data['title']
            content  = data['content']
            question = Question.objects.filter(id=question_id, user=request.user)
            question.update(title=title, content=content)
            
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
        
        except Question.DoesNotExist:
            return JsonResponse({"MESSAGE":"QUESTION_DOES_NOT_EXIST"}, status=404)

        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

    @signin_decorator
    def delete(self, request, question_id):
        try:
            if not request.user == Question.objects.get(id=question_id).user:
                return JsonResponse({"MESSAGE":"NOT_MATCHED_USER"}, status=401)
            question = Question.objects.filter(id=question_id, user=request.user)
            question.delete()
            
            return JsonResponse({"MESSAGE":"DELETE"}, status=204)
            
        except Question.DoesNotExist:
            return JsonResponse({"MESSAGE":"QUESTION_DOES_NOT_EXIST"}, status=404)

class CommentView(View):
    @signin_decorator
    def post(self, request, question_id):
        try:
            data     = json.loads(request.body)
            user     = request.user
            question = get_object_or_404(Question, id=question_id)
            content  = data['content']

            if content == None:
                return JsonResponse({"MESSAGE":"EMPTY_CONTENT"})

            Comment.objects.create(
                user     = user,
                question = question,
                content  = content
            )
            
            return JsonResponse({"MESSAGE": "CREATE"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
    
    @signin_decorator
    def get(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        comments = Comment.objects.filter(question=question_id)

        Result = [{
            "content" : comment.content
        }for comment in comments]

        return JsonResponse({"Title": question.title, "Rusult": Result}, status=200)

class QuestionSearchView(View):
    @signin_decorator
    def get(self, request):
        title_search   = request.GET.get("title")
        content_search = request.GET.get('content')
        questions      = Question.objects.all()

        if title_search:
            questions = questions.filter(title__contains=title_search)
        
        if content_search:
            questions = questions.filter(content__contains=content_search)

        Result = [{
            "title"      : question.title,
            "content"    : question.content,
            "user"       : question.user.user_id,
            "created_at" : question.created_at.strftime('%Y-%m-%d')
        }for question in questions]

        return JsonResponse({"Result":Result}, status=200)

class LikeView(View):
    @signin_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            question_id = data['question_id']
            user        = request.user
            like        = Like.objects.filter(user=user, question=question_id)
            question    = get_object_or_404(Question, id=question_id)
        
            if not like.exists():
                Like.objects.create(
                    user_id     = user.id,
                    question_id = question_id
                )
                print(like)
                question.like_count += 1
                question.save()

                return JsonResponse({"MESSAGE":"LIKE"}, status=201)

            else:
                like.delete()
                question.like_count -= 1
                question.save()

                return JsonResponse({"MESSAGE":"LIKE_CANCEL"}, status=201)

        except Question.DoesNotExist:
            return JsonResponse({"MESSAGE":"QUESTION_DOES_NOT_EXIST"}, status=404)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status=400)

    @signin_decorator
    def get(self, request):
        year      = request.GET.get("year")
        month     = request.GET.get("month")
        questions = Question.objects.filter(created_at__year=year, created_at__month=month)
        if not questions.exists():
            return JsonResponse({"MESSAGE":"QUESTION_DOES_NOT_EXIST"}, status=404)
        
        max_count = questions.aggregate(max_count=Max('like_count'))
        max_like = max_count['max_count']
                
        Result = [{
                "title"      : question.title,
                "content"    : question.content,
                "user"       : question.user.user_id,
                "created_at" : question.created_at.strftime('%Y-%m-%d')
            }for question in questions if question.like_count==max_like]
        
        return JsonResponse({"Result":Result}, status=200)