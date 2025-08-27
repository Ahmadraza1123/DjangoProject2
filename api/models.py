from django.db import models

class Blog(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField()
    author = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30)
    published = models.BooleanField(default=True)



class Comment(models.Model):
    blog = models.ForeignKey(Blog, related_name='comments', on_delete=models.CASCADE)
    comment_name = models.CharField(max_length=30)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)