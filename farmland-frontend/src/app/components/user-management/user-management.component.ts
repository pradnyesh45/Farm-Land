import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../services/user/user.service';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-user-management',
  imports: [CommonModule, FormsModule],
  templateUrl: './user-management.component.html',
  styleUrl: './user-management.component.scss',
})
export class UserManagementComponent {
  users: any[] = [];
  newUser = { username: '', password: '' };
  isAdminAccount = false;
  isLoading = false;
  error = '';
  success = '';

  constructor(
    private userService: UserService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    this.loadUsers();
  }

  loadUsers() {
    if (this.canViewUsers()) {
      this.userService.getAllUsers().subscribe({
        next: (response) => {
          this.users = response.data;
        },
        error: (error) => {
          this.error = error.error?.msg || 'Failed to load users';
        },
      });
    }
  }

  createAccount() {
    if (!this.newUser.username || !this.newUser.password) {
      this.error = 'Please fill in all fields';
      return;
    }

    this.isLoading = true;
    this.error = '';
    this.success = '';

    const createObservable = this.isAdminAccount
      ? this.userService.createAdmin(this.newUser)
      : this.userService.createUser(this.newUser);

    createObservable.subscribe({
      next: (response) => {
        this.success = response.msg;
        this.newUser = { username: '', password: '' };
        this.isAdminAccount = false;
        this.loadUsers();
        this.isLoading = false;
      },
      error: (error) => {
        this.error = error.error?.msg || 'Failed to create account';
        this.isLoading = false;
      },
    });
  }

  deleteUser(user: any) {
    if (confirm('Are you sure you want to delete this user?')) {
      const deleteObservable =
        user.role === 'Admin'
          ? this.userService.deleteAdmin(user.id) // Use admin endpoint for admins
          : this.userService.deleteUser(user.id); // Use user endpoint for regular users

      deleteObservable.subscribe({
        next: () => {
          this.success = `${user.role} deleted successfully`;
          this.loadUsers();
        },
        error: (error) => {
          this.error = error.error?.msg || 'Failed to delete user';
        },
      });
    }
  }

  canCreateAccounts(): boolean {
    const role = this.authService.getUserRole();
    return role === 'Admin' || role === 'SuperUser';
  }

  isSuperUser(): boolean {
    return this.authService.getUserRole() === 'SuperUser';
  }

  canViewUsers(): boolean {
    return this.canCreateAccounts();
  }

  canDeleteUser(user: any): boolean {
    const currentRole = this.authService.getUserRole();
    return (
      (currentRole === 'Admin' && user.role === 'User') ||
      (currentRole === 'SuperUser' && ['User', 'Admin'].includes(user.role))
    );
  }
}
