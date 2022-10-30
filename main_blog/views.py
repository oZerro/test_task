import json

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (
    Post,
    Followers
)
from .serializers import (
    PostSerializers,
    UserRegistrSerializer,
    UsersListSerializers,
    FollowingSerializer
)


class PostsOneUserAPI(APIView):
    """Вывод постов одного пользователя отсортированнных по дате
    """
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        queryset = Post.objects.filter(user=pk).order_by('-date')
        return Response(
            {'post_one_user': PostSerializers(queryset, many=True).data},
            status=200,
        )


class ListUsersSortedCountPostsAPI(APIView):
    """Вывод списка пользователей отсортированных
       по количеству постов
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all().order_by('-count_posts')
        return Response(
            {'users_sorted': UsersListSerializers(queryset, many=True).data},
            status=200,
        )


class ListUsersAPIView(APIView):
    """ Вывод списка всех пользователей
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        queryset = User.objects.exclude(id=user_id)
        return Response({
            'all_users': UsersListSerializers(queryset, many=True).data
        })



class ListFollowersAPIVIew(APIView):
    """ Вывод списка подписчиков пользователя
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
         queryset = Followers.objects.filter(following_user_id=self.request.user.id)
         arr = []
         for key in queryset:
             arr.append(get_object_or_404(User, id=key.user_id.id))

         return Response({
             'followers': UsersListSerializers(arr, many=True).data
         })



class AddFolowerView(APIView):
    """Добавление в подписчики
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = get_object_or_404(User, id=pk)
        try:
            Followers.objects.create(
                user_id=user,
                following_user_id=request.user
            )
            return Response(status=200)
        except:
            return Response(
                {'answer': 'на этого пользователя уже подписан'},
                status=400
            )


class UnFollowView(APIView):
    """Для отмены подписки
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            folowers = get_object_or_404(Followers, user_id=pk)
            folowers.delete()
        except:
            return Response(
                {"ошибка": "Вы не подписаны на этого пользователя"},
                status=400,
            )

        return Response(
            {"готово": "Подписка отменена"},
            status=200,
        )


class ListPostMyFollow(APIView):
    """Посты моих подписчиков отсортированные по дате
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Followers.objects.filter(following_user_id=self.request.user.id)
        arr = []
        for key in queryset:
            arr.extend(Post.objects.filter(user_id=key.user_id.id).order_by('-date'))



        return Response({
            'post_my_follow': PostSerializers(arr, many=True).data
        })


class MyPostAPIView(APIView):
    """ Вывод постов только активного пользователя
    """
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_id = request.user.id
        queryset = Post.objects.filter(user=user_id)
        return Response({'my_posts': PostSerializers(queryset, many=True).data})


class PostAPIView(generics.ListCreateAPIView):
    """Для просмотра и добавления постов
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializers
    permission_classes = [IsAuthenticated]


class RegistrUserView(generics.CreateAPIView):
    # Добавляем в queryset
    queryset = User.objects.all()
    # Добавляем serializer UserRegistrSerializer
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)

