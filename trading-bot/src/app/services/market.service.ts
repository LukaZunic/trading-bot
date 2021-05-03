import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MarketService {

  marketData$: Observable<any>;

  constructor(private http: HttpClient) {
    this.marketData$ = this.http.get('http://localhost:3014/');
  }




}
