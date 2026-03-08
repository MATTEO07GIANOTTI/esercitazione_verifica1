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
    await this.keycloak.init({ onLoad: 'login-required', checkLoginIframe: false });
  }

  get token(): string | undefined {
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
