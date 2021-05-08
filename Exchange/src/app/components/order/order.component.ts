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

  }

  // tslint:disable-next-line:typedef
  startBot(){
    console.log('starting bot');
    this.market.initializeBot('DOGE-USD', 'MACD', 10000).subscribe(
      (data) => console.log(data)
    );
  }

}
