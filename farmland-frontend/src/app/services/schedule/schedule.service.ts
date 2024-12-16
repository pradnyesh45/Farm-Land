import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { ApiResponse } from '../../interfaces/auth';
import { DueSchedules } from '../../interfaces/schedule';

@Injectable({
  providedIn: 'root',
})
export class ScheduleService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getDueSchedules(): Observable<ApiResponse<DueSchedules>> {
    return this.http.get<ApiResponse<DueSchedules>>(
      `${this.apiUrl}/schedules/due`
    );
  }

  getAllSchedules(): Observable<ApiResponse<any[]>> {
    return this.http.get<ApiResponse<any[]>>(`${this.apiUrl}/schedules`);
  }

  getScheduleById(id: number): Observable<ApiResponse<any>> {
    return this.http.get<ApiResponse<any>>(`${this.apiUrl}/schedules/${id}`);
  }

  getFarmSchedules(farmId: number): Observable<ApiResponse<any[]>> {
    return this.http.get<ApiResponse<any[]>>(
      `${this.apiUrl}/farms/${farmId}/schedules`
    );
  }

  getFarmerSchedules(farmerId: number): Observable<ApiResponse<any[]>> {
    return this.http.get<ApiResponse<any[]>>(
      `${this.apiUrl}/farmers/${farmerId}/schedules/all`
    );
  }

  searchSchedules(
    startDate: string,
    endDate: string,
    farmId?: number
  ): Observable<ApiResponse<any[]>> {
    let url = `${this.apiUrl}/schedules/search?start_date=${startDate}&end_date=${endDate}`;
    if (farmId) {
      url += `&farm_id=${farmId}`;
    }
    return this.http.get<ApiResponse<any[]>>(url);
  }

  createSchedule(schedule: any): Observable<ApiResponse<any>> {
    return this.http.post<ApiResponse<any>>(
      `${this.apiUrl}/schedules`,
      schedule
    );
  }

  updateSchedule(id: number, schedule: any): Observable<ApiResponse<any>> {
    return this.http.put<ApiResponse<any>>(
      `${this.apiUrl}/schedules/${id}`,
      schedule
    );
  }

  deleteSchedule(id: number): Observable<ApiResponse<any>> {
    return this.http.delete<ApiResponse<any>>(`${this.apiUrl}/schedules/${id}`);
  }
}
