from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


from django.db.models import Sum

class Author(models.Model):
    AuthorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)
    dateCreation = models.DateTimeField(auto_now_add=True)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum("rating")) or {"postRating": 0}
        pRat = postRat["postRating"]

        commentRat = self.AuthorUser.comment_set.aggregate(commentRating=Sum("rating")) or {"commentRating": 0}
        cRat = commentRat["commentRating"]

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length = 64,unique = True)


class Post(models.Model):
    author = models.ForeignKey(Author,on_delete = models.CASCADE)
    NEWS = "NW"
    ARTICLE = "AR"
    CATEGORY_CHOICES = ((NEWS,"Новость"),(ARTICLE,"Статья"))
    category_type = models.CharField(max_length = 2,choices = CATEGORY_CHOICES,default = ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add = True)
    postCategory = models.ManyToManyField(Category, through = "PostCategory")
    title = models.CharField(max_length = 128)
    text = models.TextField()
    rating = models.SmallIntegerField(default = 0)

    def like(self):
        self.rating +=1
        self.save()
    def dislike(self):
        self.rating -=1
        self.save()
    def preview(self):
        return self.text[0:123] + "..."


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post,on_delete = models.CASCADE)
    CategoryThrough = models.ForeignKey(Category,on_delete = models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post,on_delete = models.CASCADE)
    commentUser = models.ForeignKey(User,on_delete = models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add = True)
    rating = models.SmallIntegerField(default = 0)


    def like(self):
        self.rating +=1
        self.save()
    def dislike(self):
        self.rating -=1
        self.save()
    def preview(self):
        return self.text[0:123] + "..."
