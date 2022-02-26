from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.SmallIntegerField(default=0)

    def update_rating(self):
        # Рейтинг постов автора
        rating_post = self.post_set.aggregate(rat_post=Sum('rating'))
        rat_p = 0
        rat_p += rating_post.get('rat_post')

        # Рейтинг комментариев автора
        rating_comment_author = self.author_user.comment_set.aggregate(rat_comment_author=Sum('rating'))
        rat_c_a = 0
        rat_c_a += rating_comment_author.get('rat_comment_author')

        # Рейтинг комментариев под постом
        rat_c_p = 0
        all_post_author = self.post_set.all()
        for i in all_post_author:
            sum_rat_com_post = i.comment_set.aggregate(rat_comment_post=Sum('rating'))
            rat_c_p += sum_rat_com_post.get('rat_comment_post')

        self.rating_author = rat_p * 3 + rat_c_a + rat_c_p
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )

    category_type = models.CharField(max_length=2, choices=CATEGORY, default=ARTICLE)
    time_in = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'


class PostCategory(models.Model):
    _post = models.ForeignKey(Post, on_delete=models.CASCADE)
    _category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
