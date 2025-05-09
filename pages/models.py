from django.db import models

# Género del libro
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# Autor del libro
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Editorial
class Publisher(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    founded = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

# Libro
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    publication_year = models.PositiveIntegerField()
    isbn = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
