import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FarmService } from '../../../services/farm/farm.service';
import { FarmerService } from '../../../services/farmer/farmer.service';
import { AuthService } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-farm-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './farm-management.component.html',
  styleUrl: './farm-management.component.scss',
})
export class FarmManagementComponent implements OnInit {
  farms: any[] = [];
  farmers: any[] = [];
  currentFarm = {
    farmer_id: null,
    village: '',
    area: null,
    crop_grown: '',
  };
  editingFarm: any = null;
  isLoading = false;
  error = '';
  success = '';

  constructor(
    private farmService: FarmService,
    private farmerService: FarmerService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.loadFarms();
    this.loadFarmers();
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

  getFarmerName(farmerId: number): string {
    const farmer = this.farmers.find((f) => f.id === farmerId);
    return farmer ? farmer.name : 'Unknown Farmer';
  }

  saveFarm() {
    if (
      !this.currentFarm.farmer_id ||
      !this.currentFarm.village ||
      !this.currentFarm.area ||
      !this.currentFarm.crop_grown
    ) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.error = '';
    this.success = '';

    const observable = this.editingFarm
      ? this.farmService.updateFarm(this.editingFarm.id, this.currentFarm)
      : this.farmService.createFarm(this.currentFarm);

    observable.subscribe({
      next: (response: any) => {
        this.success = response.msg;
        this.resetForm();
        this.loadFarms();
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to save farm';
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  editFarm(farm: any) {
    this.editingFarm = farm;
    this.currentFarm = {
      farmer_id: farm.farmer_id,
      village: farm.village,
      area: farm.area,
      crop_grown: farm.crop_grown,
    };
  }

  cancelEdit() {
    this.resetForm();
  }

  deleteFarm(farm: any) {
    if (confirm(`Are you sure you want to delete this farm?`)) {
      this.farmService.deleteFarm(farm.id).subscribe({
        next: (response: any) => {
          this.success = response.msg;
          this.loadFarms();
        },
        error: (error: any) => {
          this.error = error.error?.msg || 'Failed to delete farm';
        },
      });
    }
  }

  resetForm() {
    this.currentFarm = {
      farmer_id: null,
      village: '',
      area: null,
      crop_grown: '',
    };
    this.editingFarm = null;
    this.error = '';
    this.success = '';
  }

  isAdmin(): boolean {
    const role = this.authService.getUserRole();
    return role === 'Admin' || role === 'SuperUser';
  }
}
