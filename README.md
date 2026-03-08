# Registro Elettronico (Angular + Flask + Keycloak)

Progetto full-stack con autenticazione Keycloak e ruoli `docente` e `studente`.

## Struttura progetto

- `frontend/`: Angular app con routing, guard e componenti separati per ruolo
- `backend/`: Flask API con PyMySQL e wrapper DB
- `keycloak/realm-export.json`: esempio realm con ruoli
- `docker-compose.yml`: stack completo (frontend, backend, mysql, keycloak)

## Funzionalità

### Docente
- Inserimento voto (`nome studente`, `materia`, `voto`)
- Visualizzazione di tutti i voti

### Studente
- Visualizzazione solo dei propri voti

## Avvio rapido (Docker)

```bash
docker compose up --build
```

Servizi:
- Frontend: http://localhost:4200
- Backend: http://localhost:5000
- Keycloak: http://localhost:8080
- MySQL: localhost:3306

## Configurazione Keycloak

1. Crea/Importa il realm usando `keycloak/realm-export.json`
2. Crea utenti con ruolo realm:
   - `docente`
   - `studente`
3. Nel frontend aggiorna `frontend/src/environments/environment.ts` con URL e client id.

## API backend

- `GET /health`
- `GET /grades` (docente: tutti i voti, studente: solo propri)
- `POST /grades` (solo docente)

Le API richiedono bearer token Keycloak (JWT) con ruoli realm.
