from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Author(models.Model):
    rating = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(models.Sum('rating'))['rating__sum'] * 3
        author_comment_rating = Comment.objects.filter(user=self.user).aggregate(models.Sum('rating'))['rating__sum']
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum']
        self.rating = post_rating + author_comment_rating + post_comment_rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name.title()}'


article = 'AR'
news = 'NW'

content_type = [
    (article, "Статья"),
    (news, 'Новость')
]


class Post(models.Model):
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    type = models.CharField(max_length=2, choices=content_type)
    date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:123] + '...'

    def __str__(self):
        return f'{self.text}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)


class Comment(models.Model):
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f'{self.text}'
