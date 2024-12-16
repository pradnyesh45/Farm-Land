import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FarmerManagementComponent } from './farmer-management.component';

describe('FarmerManagementComponent', () => {
  let component: FarmerManagementComponent;
  let fixture: ComponentFixture<FarmerManagementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FarmerManagementComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FarmerManagementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
