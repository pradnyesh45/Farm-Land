import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ScheduleService } from '../../../services/schedule/schedule.service';
import { FarmService } from '../../../services/farm/farm.service';
import { FarmerService } from '../../../services/farmer/farmer.service';
import { AuthService } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-schedule-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './schedule-management.component.html',
  styleUrl: './schedule-management.component.scss',
})
export class ScheduleManagementComponent implements OnInit {
  schedules: any[] = [];
  farms: any[] = [];
  farmers: any[] = [];
  currentSchedule = {
    farm_id: null,
    days_after_sowing: null,
    fertilizer_type: '',
    quantity: null,
    quantity_unit: '',
  };
  editingSchedule: any = null;
  isLoading = false;
  error = '';
  success = '';

  constructor(
    private scheduleService: ScheduleService,
    private farmService: FarmService,
    private farmerService: FarmerService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.loadSchedules();
    this.loadFarms();
    this.loadFarmers();
  }

  loadSchedules() {
    this.scheduleService.getAllSchedules().subscribe({
      next: (response: any) => {
        this.schedules = response.data;
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to load schedules';
      },
    });
  }

  loadFarms() {
    this.farmService.getAllFarms().subscribe({
      next: (response: any) => {
        this.farms = response.data;
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to load farms';
      },
    });
  }

  loadFarmers() {
    this.farmerService.getAllFarmers().subscribe({
      next: (response: any) => {
        this.farmers = response.data;
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to load farmers';
      },
    });
  }

  getFarmById(farmId: number) {
    return this.farms.find((f) => f.id === farmId);
  }

  getFarmerById(farmerId: number) {
    return this.farmers.find((f) => f.id === farmerId);
  }

  getFarmLabel(farm: any): string {
    if (!farm) return 'Unknown Farm';
    const farmer = this.getFarmerById(farm.farmer_id);
    return `${farmer?.name || 'Unknown Farmer'} - ${farm.village} (${
      farm.crop_grown
    })`;
  }

  saveSchedule() {
    if (
      !this.currentSchedule.farm_id ||
      !this.currentSchedule.days_after_sowing ||
      !this.currentSchedule.fertilizer_type ||
      !this.currentSchedule.quantity ||
      !this.currentSchedule.quantity_unit
    ) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.error = '';
    this.success = '';

    const observable = this.editingSchedule
      ? this.scheduleService.updateSchedule(
          this.editingSchedule.id,
          this.currentSchedule
        )
      : this.scheduleService.createSchedule(this.currentSchedule);

    observable.subscribe({
      next: (response: any) => {
        this.success = response.msg;
        this.resetForm();
        this.loadSchedules();
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to save schedule';
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  editSchedule(schedule: any) {
    this.editingSchedule = schedule;
    this.currentSchedule = {
      farm_id: schedule.farm_id,
      days_after_sowing: schedule.days_after_sowing,
      fertilizer_type: schedule.fertilizer_type,
      quantity: schedule.quantity,
      quantity_unit: schedule.quantity_unit,
    };
  }

  cancelEdit() {
    this.resetForm();
  }

  deleteSchedule(schedule: any) {
    if (confirm('Are you sure you want to delete this schedule?')) {
      this.scheduleService.deleteSchedule(schedule.id).subscribe({
        next: (response: any) => {
          this.success = response.msg;
          this.loadSchedules();
        },
        error: (error: any) => {
          this.error = error.error?.msg || 'Failed to delete schedule';
        },
      });
    }
  }

  resetForm() {
    this.currentSchedule = {
      farm_id: null,
      days_after_sowing: null,
      fertilizer_type: '',
      quantity: null,
      quantity_unit: '',
    };
    this.editingSchedule = null;
    this.error = '';
    this.success = '';
  }

  isAdmin(): boolean {
    const role = this.authService.getUserRole();
    return role === 'Admin' || role === 'SuperUser';
  }
}
