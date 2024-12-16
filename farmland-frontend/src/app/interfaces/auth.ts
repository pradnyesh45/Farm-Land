export interface LoginCredentials {
  username: string;
  password: string;
}

export interface SignupCredentials {
  username: string;
  password: string;
}

export interface User {
  id: number;
  username: string;
  role: string;
}

export interface ApiResponse<T> {
  data: T;
  msg: string;
}

export interface LoginResponseData {
  access_token: string;
  user: User;
}

export enum UserRole {
  USER = 'User',
  ADMIN = 'Admin',
  SUPER_USER = 'SuperUser',
}
