import { Component, OnInit } from '@angular/core';
import { FarmerService } from '../../../services/farmer/farmer.service';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-farmer-bill',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './farmer-bill.component.html',
  styleUrl: './farmer-bill.component.scss',
})
export class FarmerBillComponent implements OnInit {
  bill: any;
  isLoading = false;
  error = '';

  constructor(
    private farmerService: FarmerService,
    private route: ActivatedRoute
  ) {}

  ngOnInit() {
    const farmerId = this.route.snapshot.params['id'];
    this.loadBill(farmerId);
  }

  loadBill(farmerId: number) {
    this.isLoading = true;
    this.farmerService.getFarmerBill(farmerId).subscribe({
      next: (response: any) => {
        this.bill = response.data;
        this.isLoading = false;
      },
      error: (error: any) => {
        this.error = error.error?.msg || 'Failed to load bill';
        this.isLoading = false;
      },
    });
  }
}
