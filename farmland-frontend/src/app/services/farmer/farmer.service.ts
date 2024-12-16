import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { Farmer, FarmerBill } from '../../interfaces/farmer';
import { ApiResponse } from '../../interfaces/auth';

@Injectable({
  providedIn: 'root',
})
export class FarmerService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getFarmerBill(farmerId: number): Observable<ApiResponse<FarmerBill>> {
    return this.http.get<ApiResponse<FarmerBill>>(
      `${this.apiUrl}/farmers/${farmerId}/bill`
    );
  }

  getFarmersByCrop(cropType: string): Observable<ApiResponse<Farmer[]>> {
    return this.http.get<ApiResponse<Farmer[]>>(
      `${this.apiUrl}/farmers/by-crop/${cropType}`
    );
  }

  getAllFarmers(): Observable<ApiResponse<Farmer[]>> {
    return this.http.get<ApiResponse<Farmer[]>>(`${this.apiUrl}/farmers`);
  }

  getFarmerById(farmerId: number): Observable<ApiResponse<Farmer>> {
    return this.http.get<ApiResponse<Farmer>>(
      `${this.apiUrl}/farmers/${farmerId}`
    );
  }

  addFarmer(farmer: any): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.apiUrl}/farmers`, farmer);
  }

  updateFarmer(id: number, farmer: any): Observable<ApiResponse<any>> {
    return this.http.put<ApiResponse<any>>(
      `${this.apiUrl}/farmers/${id}`,
      farmer
    );
  }

  deleteFarmer(id: number): Observable<ApiResponse<any>> {
    return this.http.delete<ApiResponse<any>>(`${this.apiUrl}/farmers/${id}`);
  }
}
