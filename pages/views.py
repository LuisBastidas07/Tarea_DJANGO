from django.views.generic import ListView, DetailView
from .models import Book
from rest_framework import viewsets
from .models import Genre, Author, Publisher, Book
from .serializers import GenreSerializer, AuthorSerializer, PublisherSerializer, BookSerializer


class ListTodo(ListView):
    model = Book
    template_name = "pages/book_list.html"
    context_object_name = "books"

class DetailTodo(DetailView):
    model = Book
    template_name = "pages/book_detail.html"
    context_object_name = "book"
    

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
