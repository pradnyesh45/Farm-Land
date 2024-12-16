import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ApiResponse } from '../../interfaces/auth';

@Injectable({
  providedIn: 'root',
})
export class FarmService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getAllFarms(): Observable<ApiResponse<any[]>> {
    return this.http.get<ApiResponse<any[]>>(`${this.apiUrl}/farms`);
  }

  getFarmById(id: number): Observable<ApiResponse<any>> {
    return this.http.get<ApiResponse<any>>(`${this.apiUrl}/farms/${id}`);
  }

  createFarm(farm: any): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(`${this.apiUrl}/farms`, farm);
  }

  updateFarm(id: number, farm: any): Observable<ApiResponse<any>> {
    return this.http.put<ApiResponse<any>>(`${this.apiUrl}/farms/${id}`, farm);
  }

  deleteFarm(id: number): Observable<ApiResponse<any>> {
    return this.http.delete<ApiResponse<any>>(`${this.apiUrl}/farms/${id}`);
  }
}
