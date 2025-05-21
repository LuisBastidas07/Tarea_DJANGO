import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { BookService, Book } from '../../services/book.service';

@Component({
  selector: 'app-book-list',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    MatSnackBarModule
  ],
  template: `
    <div class="container">
      <h1 class="text-center">Books</h1>
      
      <div class="books-grid">
        <mat-card *ngFor="let book of books" class="book-card">
          <mat-card-header>
            <mat-card-title>{{book.title}}</mat-card-title>
            <mat-card-subtitle>{{book.author}}</mat-card-subtitle>
          </mat-card-header>
          <mat-card-content>
            <p>{{book.description}}</p>
            <p class="date">Created: {{book.created_at | date}}</p>
          </mat-card-content>
        </mat-card>
        
        <div *ngIf="books.length === 0" class="no-books">
          <p>No books found.</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 20px;
    }
    h1 {
      margin-bottom: 30px;
      color: #3f51b5;
    }
    .books-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 20px;
    }
    .book-card {
      height: 100%;
      display: flex;
      flex-direction: column;
    }
    mat-card-content {
      flex-grow: 1;
    }
    .date {
      color: #666;
      font-size: 0.8em;
      margin-top: 10px;
    }
    .no-books {
      grid-column: 1 / -1;
      text-align: center;
      padding: 40px;
      font-size: 18px;
      color: #666;
    }
  `]
})
export class BookListComponent implements OnInit {
  books: Book[] = [];

  constructor(
    private bookService: BookService,
    private snackBar: MatSnackBar
  ) { }

  ngOnInit(): void {
    this.loadBooks();
  }

  loadBooks(): void {
    this.bookService.getBooks().subscribe({
      next: (books) => {
        this.books = books;
      },
      error: (error) => {
        console.error('Error loading books:', error);
        this.snackBar.open('Error loading books', 'Close', { duration: 3000 });
      }
    });
  }
} 