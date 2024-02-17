import { Component } from '@angular/core';
import { UserLoginInfo } from '../../models/user';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent {
  user!: UserLoginInfo;
  email: string = "";
  password: string = "";
  token: string = "";
  
  constructor(
    private authService: AuthService, 
    private router: Router) { }

  onSubmit() {
    
    this.user = { email: this.email, password: this.password };
    this.authService.loginUser(this.user).subscribe((response) => this.token = response);

    sessionStorage.setItem('access_token', this.token);
  }

  goToMainPage() {
    this.router.navigate(['']);
  }
}
