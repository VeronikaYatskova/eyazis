import { Component, Input, OnInit, TemplateRef } from '@angular/core';
import { CategoriesComponent } from '../categories/categories.component';
import { CategoriesService } from '../../services/categories.service';
import { Category } from '../../models/category';
import { PostsComponent } from '../posts/posts.component';
import { Post } from '../../models/post';
import { PostsService } from '../../services/posts.service';
import { RouterLink, RouterOutlet } from '@angular/router';
import { ModalService } from '../../services/modal.service';

@Component({
  selector: 'app-main-section',
  standalone: true,
  imports: [
    CategoriesComponent, 
    PostsComponent, 
    RouterOutlet, 
    RouterLink],
  templateUrl: './main-section.component.html',
  styleUrl: './main-section.component.css'
})

export class MainSectionComponent implements OnInit {
  @Input() title!: string;
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
  posts: Post[] = [
    {
      id: "cf1a88ee-f330-4cf0-a4ee-923804ec4b7a",
      title: "Dapper",
      text: "Dapper is a great tool. Use it!",
      publishedDate: new Date("2024-02-15T11:51:41.408479"),
      userId: "89df5e3d-e913-4ade-8eca-506cb1c8aeba",
      categoryId: "804dec53-a273-436a-84d8-a4d857ce1f71",
      likes: 2
    },
    {
        id: "7f45003f-af1f-4fef-a392-4a020519bb16",
        title: "Dapper",
        text: "Dapper is a great tool. Use it!",
        publishedDate: new Date("2024-02-15T11:52:35.017379"),
        userId: "89df5e3d-e913-4ade-8eca-506cb1c8aeba",
        categoryId: "804dec53-a273-436a-84d8-a4d857ce1f71",
        likes: 2
    },
    {
      id: "7f45003f-af1f-4fef-a392-4a020519bb27",
      title: "Dapper",
      text: "Dapper is a great tool. Use it!",
      publishedDate: new Date("2024-02-15T11:52:35.017379"),
      userId: "89df5e3d-e913-4ade-8eca-506cb1c8aeba",
      categoryId: "b4726a6c-6072-4213-8efd-65f57cc364a8",
      likes: 2
  }
  ];

  
  constructor(
    private categoryService: CategoriesService,
    private postsService: PostsService,
    private modalService: ModalService) {}

  ngOnInit(): void {
    // this.categoryService.getCategories().subscribe((categories) => this.categories = categories);
    // this.postsService.getPosts().subscribe((response) => this.posts = response.posts);
  }

  chooseCategory(category: Category) {
    console.log(category.id);
    // this.postsService.getPostsByCategoryId(category.id).subscribe((posts) => this.posts = posts);
    this.posts = this.posts.filter((post) => post.categoryId == category.id);
    console.log(this.posts);
  }

  openModal(modalTemplate: TemplateRef<any>) {
    this.modalService.open(modalTemplate, {size: 'lg', title: 'Create Post'}).subscribe((action: any) => {
      console.log('modalAction', action);
    });
  }
}
