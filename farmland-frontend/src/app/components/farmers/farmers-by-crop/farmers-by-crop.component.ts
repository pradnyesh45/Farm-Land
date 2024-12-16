import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FarmerService } from '../../../services/farmer/farmer.service';
import { Farmer } from '../../../interfaces/farmer';
import { ApiResponse } from '../../../interfaces';

@Component({
  selector: 'app-farmers-by-crop',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './farmers-by-crop.component.html',
  styleUrl: './farmers-by-crop.component.scss',
})
export class FarmersByCropComponent {
  farmers: Farmer[] = [];
  cropType: string = '';
  isLoading = false;
  error = '';

  constructor(private farmerService: FarmerService) {}

  searchFarmers() {
    if (!this.cropType.trim()) {
      this.error = 'Please enter a crop type';
      return;
    }

    this.isLoading = true;
    this.error = '';

    this.farmerService.getFarmersByCrop(this.cropType).subscribe({
      next: (response: ApiResponse<Farmer[]>) => {
        this.farmers = response.data;
        this.isLoading = false;
      },
      error: (error) => {
        this.error = error.error?.msg || 'Failed to fetch farmers';
        this.isLoading = false;
      },
    });
  }
}
