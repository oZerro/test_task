
from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Post, Followers
from .serializers import PostSerializers


class PostsTests(APITestCase):

    def setUp(self) -> None:
        self.one_user = User.objects.create_user(
            username="test_user",
            first_name="Kola",
            last_name="Petrov",
            email="qwerty@mail.ru",
            password="qwerty123",
        )
        self.one_user.save()

        self.two_user = User.objects.create_user(
            username="test_user2",
            first_name="Kola2",
            last_name="Petrov2",
            email="qwerty2@mail.ru",
            password="qwerty123",
        )
        self.two_user.save()

        self.one_user_token = Token.objects.create(user=self.one_user)

        self.one_post = Post.objects.create(
            user=self.one_user,
            header="Test",
            text_post="test_test"
        )

        self.two_post = {
            'user': self.one_user,
            'header': "Test2",
            'text_post': "test_test2",
            'read_or_not': False,
        }

        self.tree_post = Post.objects.create(
            user=self.two_user,
            header="Test3",
            text_post="test_test3",
            read_or_not=False,
        )

    def test_posts_list_no_autorization_get(self):
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 401)

    def test_posts_list_autorization_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.one_user_token.key)
        response = self.client.get(reverse('posts'))
        self.assertEqual(response.status_code, 200)
        self.client.credentials()

    def test_posts_list_no_autorization_post(self):
        serializ = PostSerializers(self.two_post).data
        response = self.client.post(
            'posts', kwargs=serializ, format='json'
        )
        self.assertEqual(response.status_code, 404)

    def test_posts_list_autorization_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.one_user_token.key)
        serializer = PostSerializers(self.two_post).data
        url = reverse('posts')
        response = self.client.post(url, serializer)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.credentials()

    def test_list_my_post_no_autorization(self):
        # авторизуемся
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.one_user_token.key)
        # делаем пост
        serializer = PostSerializers(self.two_post).data
        url = reverse('posts')
        self.client.post(url, serializer)
        # выходим из системы
        self.client.credentials()
        # пытаемся проверить наши посты, так как мы вышли из системы получаем ошибку
        response = self.client.get(reverse('my_posts'))
        self.assertEqual(response.status_code, 401)


    def test_list_my_post_autorization(self):
        # авторизуемся
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.one_user_token.key)
        # делаем пост
        serializer = PostSerializers(self.two_post).data
        url = reverse('posts')
        self.client.post(url, serializer)
        # пытаемся проверить наши посты
        response = self.client.get(reverse('my_posts'))
        if len(response.data.get('my_posts')) == 2:
            self.assertEqual(response.status_code, 200)



