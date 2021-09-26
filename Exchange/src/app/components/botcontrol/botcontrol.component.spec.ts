import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BotcontrolComponent } from './botcontrol.component';

describe('BotcontrolComponent', () => {
  let component: BotcontrolComponent;
  let fixture: ComponentFixture<BotcontrolComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BotcontrolComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BotcontrolComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
