import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {tap} from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class MarketService {

  marketData$: Observable<any>;
  orderData$: Observable<any>;
  wallet$: Observable<any>;
  bot$: Observable<any>;
  constructor(private http: HttpClient) {
    this.marketData$ = this.http.get('http://localhost:3014/');
    this.orderData$ = this.http.get('http://localhost:3014/api/getAllOrder/');
    this.wallet$ = this.http.get('http://localhost:3014/api/getAllWallet');
    this.bot$ = this.http.get('http://localhost:3014/api/bot/getAll');
  }

  initializeBot(crypto: string, method: string, balance: number): Observable<any> {
    // const date = new Date().toISOString().slice(0, 10);
    return this.http.post(`http://localhost:3014/api/${method}/start`, {
        name: crypto,
        start_date: '2020-01-01'
    });
  }


  // tslint:disable-next-line:typedef
  createWallet(wallet_id:string,name: string, method: string, amount: string){
    return this.http.post<any>(`http://localhost:3014/api/createWallet`, {
        wallet_id:wallet_id,
        name: name,
        balance: amount,
        method:method
    }).pipe(
      tap(data => console.log('creating new wallet', data))
    );
  }

  addBot(wallet_id:string){
    return this.http.post<any>(`http://localhost:3014/api/bot/add`, {
        wallet_id:wallet_id
    }).pipe(
      tap(data => console.log('adding new bot', data))
    );
  }



}
