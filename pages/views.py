from django.views.generic import ListView, DetailView
from .models import Book

class ListTodo(ListView):
    model = Book
    template_name = "pages/book_list.html"
    context_object_name = "books"

class DetailTodo(DetailView):
    model = Book
    template_name = "pages/book_detail.html"
    context_object_name = "book"