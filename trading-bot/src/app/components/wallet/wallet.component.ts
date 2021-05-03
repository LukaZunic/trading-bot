import { Component, OnInit } from '@angular/core';
import { Wallet } from '../../interfaces/wallet';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss']
})
export class WalletComponent implements OnInit {

  wallet: Wallet;
  marketData$: Observable<any>;

  constructor(public market: MarketService) { }

  ngOnInit(): void {

    this.wallet = {
      balance: 10,
      crypto: [
        {
          name: 'cr1',
          value: 200,
          amount: 20
        }
      ]
    };

    this.marketData$ = this.market.marketData$;

  }



}
