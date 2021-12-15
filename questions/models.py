from django.db import models

class Question(models.Model):
    title      = models.CharField(max_length=50)
    content    = models.TextField()
    like_count = models.PositiveIntegerField(default=0)
    user_like  = models.ManyToManyField('users.User', through = 'Like', related_name = 'questions', blank=True)
    user       = models.ForeignKey("users.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'questions'

class Like(models.Model):
    user     = models.ForeignKey("users.User", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)

    class Meta:
        db_table = 'likes'

class Comment(models.Model):
    content  = models.TextField()
    user     = models.ForeignKey('users.User', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    class Meta:
        db_table = 'comments'