import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { OrderComponent } from './components/order/order.component';
import { WalletComponent } from './components/wallet/wallet.component';

const routes: Routes = [
  {
    path: 'wallet',
    component: WalletComponent
  },
  {
    path: 'order',
    component: OrderComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
