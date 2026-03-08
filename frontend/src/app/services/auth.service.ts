import { Injectable } from '@angular/core';
import Keycloak from 'keycloak-js';
import { environment } from '../../environments/environment';

@Injectable()
export class AuthService {
  private keycloak = new Keycloak({
    url: environment.keycloak.url,
    realm: environment.keycloak.realm,
    clientId: environment.keycloak.clientId
  });

  async init() {
    console.log('AuthService: Initializing Keycloak...');
    await this.keycloak.init({ onLoad: 'login-required', checkLoginIframe: false });
    console.log('AuthService: Keycloak initialized');
    console.log('AuthService: Initial token:', this.keycloak.token ? this.keycloak.token.substring(0, 50) + '...' : 'NO TOKEN');
  }

  get token(): string | undefined {
    console.log('AuthService.token getter called');
    console.log('AuthService: keycloak.token available?', !!this.keycloak.token);
    return this.keycloak.token;
  }

  get username(): string {
    return this.keycloak.tokenParsed?.['preferred_username'] || '';
  }

  hasRole(role: string): boolean {
    const roles = this.keycloak.tokenParsed?.['realm_access']?.roles ?? [];
    return roles.includes(role);
  }

  logout() {
    this.keycloak.logout({ redirectUri: window.location.origin });
  }
}
