import { Routes } from '@angular/router';
import { LoginComponent } from './components/auth/login/login.component';
import { ScheduleDashboardComponent } from './components/schedules/schedule-dashboard/schedule-dashboard.component';
import { authGuard } from './guards/auth.guard';
import { FarmersByCropComponent } from './components/farmers/farmers-by-crop/farmers-by-crop.component';
import { HomeComponent } from './components/home/home.component';
import { FarmerBillComponent } from './components/farmers/farmer-bill/farmer-bill.component';
import { FarmerSearchComponent } from './components/farmers/farmer-search/farmer-search.component';
import { UserManagementComponent } from './components/user-management/user-management.component';
import { FarmerManagementComponent } from './components/farmers/farmer-management/farmer-management.component';
import { FarmManagementComponent } from './components/farms/farm-management/farm-management.component';
import { ScheduleManagementComponent } from './components/schedules/schedule-management/schedule-management.component';

export const routes: Routes = [
  // { path: '', redirectTo: '', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  {
    path: '',
    component: HomeComponent,
    canActivate: [authGuard],
  },

  {
    path: 'schedules/due',
    component: ScheduleDashboardComponent,
    canActivate: [authGuard],
  },
  {
    path: 'farmers/by-crop',
    component: FarmersByCropComponent,
    canActivate: [authGuard],
  },
  {
    path: 'farmers/:id/bill',
    component: FarmerBillComponent,
    canActivate: [authGuard],
  },
  {
    path: 'farmers/search',
    component: FarmerSearchComponent,
    canActivate: [authGuard],
  },
  {
    path: 'users/manage',
    component: UserManagementComponent,
    canActivate: [authGuard],
  },
  {
    path: 'farmers/manage',
    component: FarmerManagementComponent,
    canActivate: [authGuard],
  },
  {
    path: 'farms/manage',
    component: FarmManagementComponent,
    canActivate: [authGuard],
  },
  {
    path: 'schedules/manage',
    component: ScheduleManagementComponent,
    canActivate: [authGuard],
  },
  { path: '**', redirectTo: '' },
];
