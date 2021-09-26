import { Component, OnInit } from '@angular/core';
import {MarketService} from '../../services/market.service';
import {Observable} from 'rxjs';
import {map, tap} from 'rxjs/operators';

@Component({
  selector: 'app-orders',
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.scss']
})
export class OrdersComponent implements OnInit {

  orders$: Observable<any>;

  constructor(public market: MarketService) { }

  ngOnInit(): void {
    this.orders$ = this.market.orderData$.pipe(
      //tap(data => console.log(data.data)),
      map(data => data.data)
    );
  }

}
