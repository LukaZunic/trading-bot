var express 		  = require('express');
var router 			  = express.Router();
var order             = require('./order.js');
var wallet             = require('./wallet.js');

/* ORDER */
router.post('/api/order',               order.order);
router.get('/api/getAllOrder',          order.getAllOrder);

/* WALLET */
router.post('/api/createWallet',        wallet.createWallet);
router.get('/api/getWallet',            wallet.getWallet);
router.get('/api/getAllWallet',         wallet.getAllWallet);
router.post('/api/rebalance',           wallet.rebalance);

module.exports = router;
