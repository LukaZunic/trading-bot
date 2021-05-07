import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MarketService {

  marketData$: Observable<any>;
  orderData$: Observable<any>;
  wallet$: Observable<any>;

  constructor(private http: HttpClient) {
    this.marketData$ = this.http.get('http://localhost:3014/');
    this.orderData$ = this.http.get('http://localhost:3014/api/getAllOrder/');
    this.wallet$ = this.http.get('http://localhost:3014/api/getAllWallet');
  }

  initializeBot(crypto: string, method: string, balance: number): Observable<any> {

    // this.http.post(`http://localhost:3014/api/${bot}/script`, );
    // return this.http.post<any>(`http://localhost:3014/api/createWallet`, {
    //     name: crypto,
    //     balance,
    //     method
    // });

    // const date = new Date().toISOString().slice(0, 10);

    return this.http.post(`http://localhost:3014/api/${method}/start`, {
        name: crypto,
        start_date: '2020-01-01'
    });

  }



}
