from django.views.generic import ListView, DetailView
from .models import Book
from rest_framework import viewsets
from .models import Genre, Author, Publisher, Book
from .serializers import GenreSerializer, AuthorSerializer, PublisherSerializer, BookSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import get_user_model


class ListTodo(ListView):
    model = Book
    template_name = "pages/book_list.html"
    context_object_name = "books"

class DetailTodo(DetailView):
    model = Book
    template_name = "pages/book_detail.html"
    context_object_name = "book"
    

class GenreViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
