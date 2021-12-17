from django.urls import path
from .views import QuestionView, CommentView, QuestionSearchView, LikeView

urlpatterns = [
    path('', QuestionView.as_view()),
    path('/<int:question_id>', QuestionView.as_view()),
    path('/<int:question_id>/comments', CommentView.as_view()),
    path('/list', QuestionSearchView.as_view()),
    path('/like', LikeView.as_view()),
]