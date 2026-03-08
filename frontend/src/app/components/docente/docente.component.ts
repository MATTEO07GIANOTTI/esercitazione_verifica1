import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { GradesService } from '../../services/grades.service';
import { Grade } from '../../models/grade.model';

@Component({
  selector: 'app-docente',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './docente.component.html'
})
export class DocenteComponent implements OnInit {
  grades: Grade[] = [];
  form: Grade = { student_username: '', student_name: '', subject: '', grade: 0 };

  constructor(private gradesService: GradesService) {}

  ngOnInit() {
    this.loadGrades();
  }

  loadGrades() {
    this.gradesService.getGrades().subscribe((res) => (this.grades = res));
  }

  submit() {
    this.gradesService.addGrade(this.form).subscribe(() => {
      this.form = { student_username: '', student_name: '', subject: '', grade: 0 };
      this.loadGrades();
    });
  }
}
