import { Component, EventEmitter, OnInit, Output } from '@angular/core';
import { Category } from '../../models/category';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dropdown',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './dropdown.component.html',
  styleUrl: './dropdown.component.css'
})

export class DropdownComponent implements OnInit {
  @Output() selectCategory = new EventEmitter();

  categories: Category[] = [
    {
      id: "804dec53-a273-436a-84d8-a4d857ce1f71",
      name: "Beauty"
    },
    {
        id: "b4726a6c-6072-4213-8efd-65f57cc364a8",
        name: "SciFi"
    }
  ]; 

  ngOnInit(): void {
    
  }

  changeCategory(event: any) {
    console.log(event?.target?.value);
    this.selectCategory.emit(event?.target?.value);
  }
}
