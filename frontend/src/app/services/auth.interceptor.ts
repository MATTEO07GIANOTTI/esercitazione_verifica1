import { Injectable } from '@angular/core';
import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.authService.token;
    console.log('AuthInterceptor: token available?', !!token);
    console.log('AuthInterceptor: token value:', token ? token.substring(0, 50) + '...' : 'NO TOKEN');
    
    if (!token) {
      console.warn('AuthInterceptor: No token available, sending request without auth');
      return next.handle(req);
    }

    const modifiedReq = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
    console.log('AuthInterceptor: Added Bearer token to request');
    return next.handle(modifiedReq);
  }
}
