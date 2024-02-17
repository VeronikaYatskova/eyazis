import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Category } from '../../models/category';

@Component({
  selector: 'app-categories',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './categories.component.html',
  styleUrl: './categories.component.css'
})

export class CategoriesComponent {
  @Input() categories: Category[] = [];
  @Output() btnClick = new EventEmitter();

  onCategoryChosen(category: Category) {
    this.btnClick.emit(category);
  }
}
