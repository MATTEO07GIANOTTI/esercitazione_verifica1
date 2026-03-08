import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { GradesService } from '../../services/grades.service';
import { Grade } from '../../models/grade.model';

@Component({
  selector: 'app-studente',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './studente.component.html'
})
export class StudenteComponent implements OnInit {
  grades: Grade[] = [];
  error: string = '';
  loading: boolean = true;

  constructor(private gradesService: GradesService) {}

  ngOnInit() {
    console.log('StudenteComponent: Loading grades...');
    this.gradesService.getGrades().subscribe(
      (res) => {
        console.log('StudenteComponent: Grades loaded:', res);
        this.grades = res;
        this.loading = false;
      },
      (err) => {
        console.error('StudenteComponent: Error loading grades:', err);
        this.error = `Error: ${err.status} - ${err.statusText}`;
        this.loading = false;
      }
    );
  }
}
