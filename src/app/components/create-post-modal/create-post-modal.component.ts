import { Component, ElementRef, EventEmitter, Input, Output } from '@angular/core';
import { DropdownComponent } from '../dropdown/dropdown.component';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-create-post-modal',
  standalone: true,
  imports: [DropdownComponent, FormsModule],
  templateUrl: './create-post-modal.component.html',
  styleUrl: './create-post-modal.component.css'
})

export class CreatePostModalComponent {
  postTitle: string = "";
  postText: string = "";
  categoryId: string = "";

  @Input() size? = "md";
  @Input() title? = "Modal title";
  
  @Output() closeEvent = new EventEmitter();
  @Output() submitEvent = new EventEmitter();

  constructor(private elementRef: ElementRef) { }

  submit() {
    console.log(this.postTitle + ' ' + this.postText + ' ' + this.categoryId);

    this.elementRef.nativeElement.remove();
    this.submitEvent.emit({ title: this.postTitle, text: this.postText, categoryId: this.categoryId });
  }

  close() {
    this.elementRef.nativeElement.remove();
    this.closeEvent.emit();
  }

  categoryChange(event: any) {
    this.categoryId = event;
  }
}
