import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FarmersByCropComponent } from './farmers-by-crop.component';

describe('FarmersByCropComponent', () => {
  let component: FarmersByCropComponent;
  let fixture: ComponentFixture<FarmersByCropComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FarmersByCropComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FarmersByCropComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
