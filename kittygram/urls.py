from django.urls import include, path

# from cats.views import cat_list
# from cats.views import APICat
# from cats.views import CatList, CatDetail
from cats.views import CatViewSet, OwnerViewSet, LightCatViewSet

from rest_framework.routers import SimpleRouter


# Создаётся роутер
router = SimpleRouter()
# Вызываем метод .register с нужными параметрами
router.register('cats', CatViewSet)
router.register('owners', OwnerViewSet)
router.register(r'mycats', LightCatViewSet)

# Можно указать basename
# router.register('cats', CatViewSet, basename='tiger')
# Тогда после подстановки в УРЛах будет
# urlpatterns = [
#     path('cat/', ..., name='tiger-list'),
#     path('cat/<int:pk>/', ..., name='tiger-detail'),
# ]


# В роутере можно зарегистрировать любое количество пар "URL, viewset":
# например
# router.register('owners', OwnerViewSet)
# Но нам это пока не нужно

urlpatterns = [
   # path('cats/', cat_list),
   # path('cats/', APICat.as_view()),

   # path('cats/', CatList.as_view()),
   # path('cats/<int:pk>', CatDetail.as_view()),

   # Все зарегистрированные в router пути доступны в router.urls
   # Включим их в головной urls.py
   path('', include(router.urls)),
]


