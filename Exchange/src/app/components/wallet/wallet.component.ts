import { Component, OnInit } from '@angular/core';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {FormControl, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-wallet',
  templateUrl: './wallet.component.html',
  styleUrls: ['./wallet.component.scss']
})
export class WalletComponent implements OnInit {

  wallets$: Observable<any>;

  form: FormGroup;

  new = false;

  constructor(public market: MarketService) {
    this.form = new FormGroup({
      wallet_id: new FormControl(''),
      amount: new FormControl(''),
      method: new FormControl(''),
      name: new FormControl('')
    });
  }

  change(value:any){
    this.form.patchValue({name:value})
  }
  changeMethod(value:any){
    this.form.patchValue({method:value})
  }

  ngOnInit(): void {
    this.wallets$ = this.market.wallet$.pipe(
      map(data => data.data)
    );
  }

  // tslint:disable-next-line:typedef
  createWallet(){
    this.market.createWallet(this.form.value['wallet_id'],this.form.value['name'], this.form.value['method'], this.form.value['amount']).subscribe();
    this.market.addBot(this.form.value['wallet_id'],this.form.value['name'], this.form.value['method']).subscribe();
    this.form.patchValue({wallet_id:'',name:'', amount:'', method:''});
  
  }



}
