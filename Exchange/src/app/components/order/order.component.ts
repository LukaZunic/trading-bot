import { Component, OnInit } from '@angular/core';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-order',
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.scss']
})
export class OrderComponent implements OnInit {

  orderData$: Observable<any>;
  constructor(public order: MarketService) { }

  ngOnInit(): void {
    this.orderData$ = this.order.orderData$;
    console.log(this.orderData$);
  }

}
