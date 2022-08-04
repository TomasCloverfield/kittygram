# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# from rest_framework.generics import \
#     ListCreateAPIView,\
#     RetrieveUpdateDestroyAPIView
# from rest_framework.response import Response
# from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Cat, Owner
from .serializers import CatSerializer, OwnerSerializer, CatListSerializer

# View функции

# @api_view(['GET', 'POST'])
# def cat_list(request):
#     if request.method == 'POST':
#         # Создаём объект сериализатора
#         # и передаём в него данные из POST-запроса
#         serializer = CatSerializer(data=request.data)
#         if serializer.is_valid():
#             # Если полученные данные валидны —
#             # сохраняем данные в базу через save().
#             serializer.save()
#             # Возвращаем JSON со всеми данными нового объекта
#             # и статус-код 201
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # Если данные не прошли валидацию —
#         # возвращаем информацию об ошибках и соответствующий статус-код:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     # В случае GET-запроса возвращаем список всех котиков
#     cats = Cat.objects.all()
#     serializer = CatSerializer(cats, many=True)
#     return Response(serializer.data)


##### For Post from trainer task
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def api_posts_detail(request, pk):
#     post = Post.objects.get(id=pk)
#     if request.method == 'PUT' or request.method == 'PATCH':
#         post = Post.objects.get(id=pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         Post.objects.get(id=pk).delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     post = Post.objects.get(id=pk)
#     serializer = PostSerializer(post)
#     return Response(serializer.data, status=status.HTTP_200_OK)

# Низкоуровнеые дженерики

# class APICat(APIView):
#     def get(self, request):
#         cats = Cat.objects.all()
#         serializer = CatSerializer(cats, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = CatSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# Высокоуровнеые дженерики

# class CatList(ListCreateAPIView):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer
#
#
# class CatDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Cat.objects.all()
#     serializer_class = CatSerializer

class CatViewSet(viewsets.ModelViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    def get_serializer_class(self):
        # Если запрошенное действие (action) —
        # получение списка объектов ('list')
        if self.action == 'list':
            return CatListSerializer
        return CatSerializer

    @action(detail=False, url_path='recent-white-cats')
    def recent_white_cats(self, request):
        cats = Cat.objects.filter(color='White')[:5]
        serializer = self.get_serializer(cats, many=True)
        return Response(serializer.data)


# Собираем вьюсет, который будет уметь изменять или удалять отдельный объект.
# А ничего больше он уметь не будет.
class UpdateDeleteViewSet(
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet
):
    pass


class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    # В теле класса никакой код не нужен! Пустячок, а приятно.
    pass


class LightCatViewSet(CreateRetrieveViewSet):
    queryset = Cat.objects.all()
    serializer_class = CatSerializer




# # # Просто демонстрация из примера
# # Если бы пользователи могли оставлять комментарии к котикам,
# # то эндпоинт для работы с комментариями выглядел бы примерно так:
# # cats/{cat_id}/comments/
#
# class CommentViewSet(viewsets.ModelViewSet):
#     serializer_class = CommentSerializer
#     # queryset во вьюсете не указываем
#     # Нам тут нужны не все комментарии, а только связанные с котом с
#     # id=cat_id
#     # Поэтому нужно переопределить метод get_queryset и применить фильтр
#     def get_queryset(self):
#         # Получаем id котика из эндпоинта
#         cat_id = self.kwargs.get("cat_id")
#         # И отбираем только нужные комментарии
#         new_queryset = Comment.objects.filter(cat=cat_id)
#         return new_queryset

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
