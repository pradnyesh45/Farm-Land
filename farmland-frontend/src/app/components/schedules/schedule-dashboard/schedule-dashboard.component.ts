import { Component } from '@angular/core';
import { ScheduleResponse, Schedule } from '../../../interfaces/schedule';
import { ScheduleService } from '../../../services/schedule/schedule.service';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-schedule-dashboard',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './schedule-dashboard.component.html',
  styleUrl: './schedule-dashboard.component.scss',
})
export class ScheduleDashboardComponent {
  schedules: Schedule[] = [];
  isLoading = false;
  error = '';

  constructor(private scheduleService: ScheduleService) {}

  ngOnInit() {
    this.loadDueSchedules();
  }

  loadDueSchedules() {
    this.isLoading = true;
    this.scheduleService.getDueSchedules().subscribe({
      next: (response: ScheduleResponse) => {
        this.schedules = response.data.today_tomorrow;
        this.isLoading = false;
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to load schedules';
        this.isLoading = false;
      },
    });
  }
}
