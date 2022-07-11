from django.urls import include, path

# from cats.views import cat_list
from cats.views import APICat

urlpatterns = [
   # path('cats/', cat_list),
   path('cats/', APICat.as_view()),
]


