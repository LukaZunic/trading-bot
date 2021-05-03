import { Component, OnInit } from '@angular/core';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss']
})
export class WalletComponent implements OnInit {

  wallet$: Observable<any>;
  marketData$: Observable<any>;

  constructor(public market: MarketService) { }

  ngOnInit(): void {

    this.marketData$ = this.market.marketData$;
    this.wallet$ = this.market.wallet$;

  }



}
