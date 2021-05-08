import { Component, OnInit } from '@angular/core';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss']
})
export class WalletComponent implements OnInit {

  wallets$: Observable<any>;

  constructor(public market: MarketService) { }

  ngOnInit(): void {
    this.wallets$ = this.market.wallet$.pipe(
      map(data => data.data)
    );
  }

  // tslint:disable-next-line:typedef
  createWallet(){
    this.market.createWallet('BTC-USD', 'MACD', 10000).subscribe();
  }



}
