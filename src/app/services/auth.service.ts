import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserLoginInfo } from '../models/user';

const httpOptions = { 
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
  })
};

@Injectable({
  providedIn: 'root'
})

export class AuthService {
  appUrl: string = "http://localhost:7233/auth";
  
  constructor(private http: HttpClient) { }

  loginUser(user: UserLoginInfo): Observable<string> {
    console.log(user.email + ' ' + user.password);

    return this.http.post<string>(
      `${this.appUrl}/sign-in`, 
      user,
      httpOptions);
  }
}
