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



  constructor(public market: MarketService) {
    this.form = new FormGroup({
      take_profit: new FormControl(''),
      stop_loss: new FormControl('')
    });
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


}
