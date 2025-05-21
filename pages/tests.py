from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Book, Author, Publisher, Genre

class BookPermissionsTest(APITestCase):
    def setUp(self):
        # Crear usuarios de prueba
        self.admin_user = get_user_model().objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.normal_user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.another_user = get_user_model().objects.create_user(
            username='anotheruser',
            email='another@example.com',
            password='anotherpass123'
        )

        # Crear datos necesarios para los libros
        self.author = Author.objects.create(
            first_name='Test',
            last_name='Author'
        )
        self.publisher = Publisher.objects.create(
            name='Test Publisher',
            country='Test Country'
        )
        self.genre = Genre.objects.create(
            name='Test Genre'
        )

        # Crear un libro para el usuario normal
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            publisher=self.publisher,
            genre=self.genre,
            publication_year=2024,
            isbn='1234567890123',
            owner=self.normal_user
        )

        # URLs para las pruebas
        self.book_list_url = reverse('book-list')
        self.book_detail_url = reverse('book-detail', kwargs={'pk': self.book.pk})

    def test_unauthenticated_user_cannot_access_list(self):
        """Test que verifica que un usuario no autenticado no puede acceder a la lista de libros"""
        response = self.client.get(self.book_list_url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_unauthenticated_user_cannot_access_detail(self):
        """Test que verifica que un usuario no autenticado no puede acceder al detalle de un libro"""
        response = self.client.get(self.book_detail_url)
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_authenticated_user_can_access_list(self):
        """Test que verifica que un usuario autenticado puede acceder a la lista de libros"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_access_detail(self):
        """Test que verifica que un usuario autenticado puede acceder al detalle de un libro"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_owner_can_update_book(self):
        """Test que verifica que el propietario puede actualizar su libro"""
        self.client.force_authenticate(user=self.normal_user)
        data = {
            'title': 'Updated Title',
            'author': self.author.id,
            'publisher': self.publisher.id,
            'genre': self.genre.id,
            'publication_year': 2024,
            'isbn': '1234567890123',
            'owner': self.normal_user.id
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book.pk).title, 'Updated Title')

    def test_non_owner_cannot_update_book(self):
        """Test que verifica que un usuario que no es propietario no puede actualizar el libro"""
        self.client.force_authenticate(user=self.another_user)
        data = {
            'title': 'Updated Title',
            'author': self.author.id,
            'publisher': self.publisher.id,
            'genre': self.genre.id,
            'publication_year': 2024,
            'isbn': '1234567890123',
            'owner': self.normal_user.id
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_owner_can_delete_book(self):
        """Test que verifica que el propietario puede eliminar su libro"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())

    def test_non_owner_cannot_delete_book(self):
        """Test que verifica que un usuario que no es propietario no puede eliminar el libro"""
        self.client.force_authenticate(user=self.another_user)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Book.objects.filter(pk=self.book.pk).exists())

    def test_admin_can_access_all_books(self):
        """Test que verifica que el admin puede acceder a todos los libros"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_update_any_book(self):
        """Test que verifica que el admin puede actualizar cualquier libro"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'title': 'Admin Updated Title',
            'author': self.author.id,
            'publisher': self.publisher.id,
            'genre': self.genre.id,
            'publication_year': 2024,
            'isbn': '1234567890123',
            'owner': self.normal_user.id
        }
        response = self.client.put(self.book_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Book.objects.get(pk=self.book.pk).title, 'Admin Updated Title')

    def test_admin_can_delete_any_book(self):
        """Test que verifica que el admin puede eliminar cualquier libro"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.book_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book.pk).exists())
