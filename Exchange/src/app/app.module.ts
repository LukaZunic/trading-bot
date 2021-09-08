import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { WalletComponent } from './components/wallet/wallet.component';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { MarketComponent } from './components/market/market.component';
import { OrdersComponent } from './components/orders/orders.component';
import { GraphComponent } from './components/graph/graph.component';

import { HttpClientModule } from '@angular/common/http';
import { OrderComponent } from './components/order/order.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

/* ANGULAR MATERIAL IMPORTS */
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatButtonModule} from '@angular/material/button';
import {MatCardModule} from '@angular/material/card';
import {MatSliderModule} from '@angular/material/slider';
import {MatListModule} from '@angular/material/list';
import {ReactiveFormsModule} from '@angular/forms';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import { BotcontrolComponent } from './components/botcontrol/botcontrol.component';




@NgModule({
  declarations: [
    AppComponent,
    WalletComponent,
    OrderComponent,
    NavbarComponent,
    DashboardComponent,
    MarketComponent,
    OrdersComponent,
    GraphComponent,
    BotcontrolComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    BrowserAnimationsModule,
    MatIconModule,
    MatToolbarModule,
    MatButtonModule,
    MatSliderModule,
    MatCardModule,
    MatListModule,
    ReactiveFormsModule,
    MatSelectModule,
    MatInputModule
  ],
  providers: [
    HttpClientModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
