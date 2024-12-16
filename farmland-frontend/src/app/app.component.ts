import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './components/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, NavbarComponent],
  // templateUrl: './app.component.html',
  template: `
    <app-navbar></app-navbar>
    <main>
      <router-outlet />
    </main>
  `,
  // styleUrl: './app.component.scss',
  styles: [
    `
      main {
        padding: 20px;
      }
    `,
  ],
})
export class AppComponent {
  title = 'farmland-frontend';
}
