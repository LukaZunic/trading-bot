import { Component, OnInit } from '@angular/core';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';
import {tap} from 'rxjs/operators';

@Component({
  selector: 'app-order',
  templateUrl: './order.component.html',
  styleUrls: ['./order.component.scss']
})
export class OrderComponent implements OnInit {

  order$: Observable<any>;

  constructor(public market: MarketService) { }

  ngOnInit(): void {

    this.market.initializeBot('BTC', 'MACD', 10000).pipe(
      tap(data => console.log(data))
    ).subscribe();

  }

}
