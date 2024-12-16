import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FarmerService } from '../../../services/farmer/farmer.service';
import { AuthService } from '../../../services/auth/auth.service';

@Component({
  selector: 'app-farmer-management',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './farmer-management.component.html',
  styleUrl: './farmer-management.component.scss',
})
export class FarmerManagementComponent implements OnInit {
  farmers: any[] = [];
  currentFarmer = {
    name: '',
    phone_number: '',
    language: 'English',
  };
  editingFarmer: any = null;
  isLoading = false;
  error = '';
  success = '';

  constructor(
    private farmerService: FarmerService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.loadFarmers();
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

  saveFarmer() {
    if (
      !this.currentFarmer.name ||
      !this.currentFarmer.phone_number ||
      !this.currentFarmer.language
    ) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.error = '';
    this.success = '';

    const observable = this.editingFarmer
      ? this.farmerService.updateFarmer(
          this.editingFarmer.id,
          this.currentFarmer
        )
      : this.farmerService.addFarmer(this.currentFarmer);

    observable.subscribe({
      next: (response: any) => {
        this.success = response.msg;
        this.resetForm();
        this.loadFarmers();
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to save farmer';
      },
      complete: () => {
        this.isLoading = false;
      },
    });
  }

  editFarmer(farmer: any) {
    this.editingFarmer = farmer;
    this.currentFarmer = {
      name: farmer.name,
      phone_number: farmer.phone_number,
      language: farmer.language,
    };
  }

  cancelEdit() {
    this.resetForm();
  }

  deleteFarmer(farmer: any) {
    if (confirm(`Are you sure you want to delete ${farmer.name}?`)) {
      this.farmerService.deleteFarmer(farmer.id).subscribe({
        next: (response: any) => {
          this.success = response.msg;
          this.loadFarmers();
        },
        error: (error: any) => {
          this.error = error.error?.msg || 'Failed to delete farmer';
        },
      });
    }
  }

  resetForm() {
    this.currentFarmer = {
      name: '',
      phone_number: '',
      language: 'English',
    };
    this.editingFarmer = null;
    this.error = '';
    this.success = '';
  }

  isAdmin(): boolean {
    const role = this.authService.getUserRole();
    return role === 'Admin' || role === 'SuperUser';
  }
}
