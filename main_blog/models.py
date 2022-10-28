from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="Автор",
        null=True,
    )
    header = models.CharField(
        max_length=100,
        default="",
        verbose_name="Заголовок",
    )
    text_post = models.TextField(
        default="",
        verbose_name="Текст поста",
    )
    read_or_not = models.BooleanField(
        default=False,
        verbose_name="Прочитано?"
    )

    class Meta:
        db_table = "posts"
        ordering = ['read_or_not']
        verbose_name = "Поост"
        verbose_name_plural = "Посты"


class Followers(models.Model):
    user_id = models.ForeignKey(
        User,
        related_name="Subscribed",
        verbose_name="Тот на кого подписались",
        on_delete=models.CASCADE
    )
    following_user_id = models.ForeignKey(
        User,
        related_name="Following",
        verbose_name="Подписавшийся",
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user_id', 'following_user_id'],
                name="unique_followers",
            )
        ]
        ordering = ["-created"]