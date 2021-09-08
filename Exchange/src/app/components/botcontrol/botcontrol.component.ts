import { Component, OnInit } from '@angular/core';
import { MarketService } from '../../services/market.service';
import {Observable} from 'rxjs';
import {map} from 'rxjs/operators';
import {FormControl, FormGroup} from '@angular/forms';
@Component({
  selector: 'app-botcontrol',
  templateUrl: './botcontrol.component.html',
  styleUrls: ['./botcontrol.component.scss']
})
export class BotcontrolComponent implements OnInit {

  bots$: Observable<any>;

  form: FormGroup;

  new = false;

  constructor(public market: MarketService) {
    this.form = new FormGroup({
      take_profit: new FormControl(''),
      stop_loss: new FormControl('')
    });
  }

  change(value:any){
    //this.form.patchValue({name:value})
  }
  changeMethod(value:any){
    //this.form.patchValue({method:value})
  }
  startBot(wallet_id,name, method){
    this.market.startBot(wallet_id,name,method,this.form.value['take_profit'], this.form.value['stop_loss']).subscribe();
  }
  stopBot(wallet_id,method){
    this.market.stopBot(wallet_id,method).subscribe();
  }
  ngOnInit(): void {
    this.bots$ = this.market.bot$.pipe(
      map(data => data.data)
    );
  }

  // tslint:disable-next-line:typedef
  createWallet(){
    //this.market.createWallet(this.form.value['name'], this.form.value['method'], this.form.value['amount']).subscribe();
    //this.form.patchValue({name:'', amount:'', method:''});
  }
}
