import { Component, OnInit } from '@angular/core';
import {MarketService} from '../../services/market.service';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-market',
  templateUrl: './market.component.html',
  styleUrls: ['./market.component.scss']
})
export class MarketComponent implements OnInit {

  marketData$: Observable<any>;

  constructor(public market: MarketService) { }

  ngOnInit(): void {
    this.marketData$ = this.market.marketData$;
  }

}
