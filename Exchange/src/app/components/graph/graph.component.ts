import { Component, OnInit } from '@angular/core';
import {MarketService} from '../../services/market.service';

@Component({
  selector: 'app-graph',
  templateUrl: './graph.component.html',
  styleUrls: ['./graph.component.scss']
})
export class GraphComponent implements OnInit {

  constructor(public market: MarketService) { }

  ngOnInit(): void {

  }

}
