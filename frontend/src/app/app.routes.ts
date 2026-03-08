import { Routes } from '@angular/router';
import { DocenteComponent } from './components/docente/docente.component';
import { StudenteComponent } from './components/studente/studente.component';
import { AccessoNegatoComponent } from './components/accesso-negato/accesso-negato.component';
import { HomeComponent } from './components/home/home.component';
import { docenteGuard } from './guards/docente.guard';
import { studenteGuard } from './guards/studente.guard';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'docente', component: DocenteComponent, canActivate: [docenteGuard] },
  { path: 'studente', component: StudenteComponent, canActivate: [studenteGuard] },
  { path: 'accesso-negato', component: AccessoNegatoComponent },
  { path: '**', redirectTo: '' }
];
