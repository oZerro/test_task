from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from .models import (
    Post,
    Followers,
)


class UsersListSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'count_posts')


class FollowingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Followers
        fields = ('user_id',)


class PostSerializers(serializers.ModelSerializer):
    """Сериалайзер для добаления и просмотра всех постов
    """
    class Meta:
        model = Post
        fields = "__all__"

    def save(self, *args, **kwargs):
        post = Post(
            user=self.validated_data['user'],
            header=self.validated_data['header'],
            text_post=self.validated_data['text_post'],
            read_or_not=self.validated_data['read_or_not']
        )

        user_id = self.validated_data.get('user').id
        user = get_object_or_404(User, id=user_id)
        user.count_posts += 1
        user.save()
        post.save()
        return post


class UserRegistrSerializer(serializers.ModelSerializer):
    """Сериалайзер для регистрации пользователей
    """
    # Поле для повторения пароля
    password2 = serializers.CharField(label="Повторите пароль")

    # Настройка полей
    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']

    # Метод для сохранения нового пользователя
    def save(self, *args, **kwargs):
        # Создаём объект класса User
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
            username=self.validated_data['username'],  # Назначаем Логин
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name']
        )

        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user