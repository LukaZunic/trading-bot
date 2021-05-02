import { Component, OnInit } from '@angular/core';
import { Wallet } from '../../interfaces/wallet';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss']
})
export class WalletComponent implements OnInit {

  wallet: Wallet;

  constructor() { }

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
    }

  }

}
