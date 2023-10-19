from django.db import models  # импорт
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    rating = models.IntegerField(default=0)
    user_name = models.OneToOneField(User, on_delete=models.CASCADE)

    def update(self):

        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')
        commRat = self.user_name.comment_set.aggregate(commRating=Sum('rating'))
        cRat = 0
        cRat += commRat.get('commRating')

        self.rating = pRat *3 + cRat
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    news = "NW"
    articl = "AR"
    CHOICE_CONTENS = [(news,'Новости'), (articl,'Статья')]
    time_creates = models.DateTimeField(auto_now_add=True)
    choice_content = models.CharField(max_length=2, choices=CHOICE_CONTENS, default= news)
    tutle = models.CharField(max_length=64)
    rating = models.IntegerField(default=0)
    article_text = models.TextField()
    autor = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.article_text) <= 124:
            prev = self.article_text
        else:
            prev = self.article_text[:123]+"..."
        return prev


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    time_creates = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()