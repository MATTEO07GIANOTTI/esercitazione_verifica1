import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  template: `
    <h2>Benvenuto 👋</h2>
    <p *ngIf="auth.hasRole('docente')">Accesso docente rilevato, clicca sotto per entrare.</p>
    <p *ngIf="auth.hasRole('studente')">Accesso studente rilevato, clicca sotto per entrare.</p>
    <button (click)="goToArea()">Vai alla tua area</button>
  `
})
export class HomeComponent {
  constructor(public auth: AuthService, private router: Router) {}

  goToArea() {
    if (this.auth.hasRole('docente')) this.router.navigateByUrl('/docente');
    else if (this.auth.hasRole('studente')) this.router.navigateByUrl('/studente');
    else this.router.navigateByUrl('/accesso-negato');
  }
}
