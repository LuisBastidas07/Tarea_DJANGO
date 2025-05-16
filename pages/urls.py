from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, AuthorViewSet, PublisherViewSet, BookViewSet, ListTodo, DetailTodo

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'publishers', PublisherViewSet)
router.register(r'books', BookViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Cambiamos las rutas para que no haya conflicto con el router
    path('list/', ListTodo.as_view(), name='todo_list'),
    path('detail/<int:pk>/', DetailTodo.as_view(), name='todo_detail'),
]