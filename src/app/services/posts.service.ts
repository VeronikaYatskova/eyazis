import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AddPost, GetPosts, Post } from '../models/post';
import { HttpClient, HttpHeaders } from '@angular/common/http';

const httpOptions = { 
  headers: new HttpHeaders({
    'Authorization': 'Bearer ' + sessionStorage.getItem('access_token'),
  })
};

@Injectable({
  providedIn: 'root'
})

export class PostsService {
  apiUrl: string = "http://localhost:7233";

  constructor(private http: HttpClient) { }

  getPosts(): Observable<GetPosts> { 
    var posts = this.http.get<GetPosts>(`${this.apiUrl}/posts?page=1&pageSize=10`);

    return posts;
  }

  getPostsByCategoryId(categoryId: string): Observable<Post[]> {
    var posts = this.http.get<Post[]>(`${this.apiUrl}/posts/categories?categoryId=${categoryId}`);

    return posts;
  }

  addPost(post: AddPost): Observable<Post> {
    return this.http.post<Post>(
      `${this.apiUrl}/posts`, 
      post,
      httpOptions);;
  }
}
