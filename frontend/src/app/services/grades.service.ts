import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Grade } from '../models/grade.model';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class GradesService {
  constructor(private http: HttpClient) {}

  getGrades(): Observable<Grade[]> {
    return this.http.get<Grade[]>(`${environment.apiUrl}/grades`);
  }

  addGrade(payload: Grade): Observable<{ message: string }> {
    return this.http.post<{ message: string }>(`${environment.apiUrl}/grades`, payload);
  }
}
