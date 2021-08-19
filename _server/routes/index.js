var express 		  = require('express');
var router 			  = express.Router();
var order             = require('./order.js');
var wallet            = require('./wallet.js');
var ichimoku          = require('./ichimoku.js');  
var macd              = require('./macd.js');
var macdboll          = require('./macdboll.js');
var rsi               = require('./rsi.js')
var market            = require('./market.js');


/* ORDER */
router.post('/api/order',               order.order);
router.get('/api/getAllOrder',          order.getAllOrder);

/* WALLET */
router.post('/api/createWallet',        wallet.createWallet);
router.get('/api/getWallet',            wallet.getWallet);
router.get('/api/getAllWallet',         wallet.getAllWallet);
router.post('/api/rebalance',           wallet.rebalance);

/* ICHIMOKU */
router.post('/api/ichimoku/script',     ichimoku.ichimoku);
router.post('/api/ichimoku/start',      ichimoku.startichimoku);

/* MACD */
router.post('/api/macd/script',         macd.macd);
router.post('/api/macd/start',         macd.startmacd);

/* MACD & BOLLINGER BANDS */
router.post('/api/macdboll/script',     macdboll.macdboll);
router.post('/api/macdboll/start',      macdboll.startmacdboll);


/* RSI */
router.post('/api/rsi/script',          rsi.rsi);
router.post('/api/rsi/start',           rsi.startrsi);

/* MARKET */
router.get('/api/market',               market.market);



module.exports = router;
