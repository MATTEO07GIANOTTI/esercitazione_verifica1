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

  constructor(private gradesService: GradesService) {}

  ngOnInit() {
    this.gradesService.getGrades().subscribe((res) => (this.grades = res));
  }
}
