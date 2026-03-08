import { Component } from '@angular/core';

@Component({
  selector: 'app-accesso-negato',
  standalone: true,
  template: `
    <h2>🚫 Accesso Negato</h2>
    <p>Oops! Hai bussato alla porta sbagliata.</p>
    <p>Torna alla home e usa il percorso corretto per il tuo ruolo 😄</p>
    <a href="/">Torna alla Home</a>
  `
})
export class AccessoNegatoComponent {}
