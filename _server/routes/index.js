var express 		  = require('express');
var router 			  = express.Router();
var order             = require('./order.js');
var wallet             = require('./wallet.js');

/* ORDER */
router.post('/api/order',               order.order);
router.post('/api/getAllOrder',         order.getAllOrder);

/* WALLET */
router.post('/api/createWallet',        wallet.createWallet);
router.post('/api/getWallet',           wallet.getWallet);
router.post('/api/getAllWallet',        wallet.getAllWallet);
router.post('/api/rebalance',           wallet.rebalance);

module.exports = router;