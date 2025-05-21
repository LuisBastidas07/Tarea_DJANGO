from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BookViewSet, UserViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register('books', BookViewSet, basename='books')

urlpatterns = [
    path('', include(router.urls)),
]