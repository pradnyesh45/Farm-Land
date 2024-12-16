import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FarmerService } from '../../../services/farmer/farmer.service';
import { Farmer } from '../../../interfaces/farmer';
import { FormsModule } from '@angular/forms';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-farmer-search',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './farmer-search.component.html',
  styleUrl: './farmer-search.component.scss',
})
export class FarmerSearchComponent {
  farmers: Farmer[] = [];
  isLoading = false;
  error = '';

  constructor(private farmerService: FarmerService) {}

  ngOnInit() {
    this.loadAllFarmers();
  }

  loadAllFarmers() {
    this.isLoading = true;
    this.farmerService.getAllFarmers().subscribe({
      next: (response) => {
        this.farmers = response.data;
        this.isLoading = false;
      },
      error: (error) => {
        this.error = error.error?.msg || 'Failed to load farmers';
        this.isLoading = false;
      },
    });
  }
}
