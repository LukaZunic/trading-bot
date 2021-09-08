var express 		  = require('express');
var router 			  = express.Router();
var order             = require('./order.js');
var wallet            = require('./wallet.js');
var ichimoku          = require('./ichimoku.js');  
var macd              = require('./macd.js');
var rsi               = require('./rsi.js')
var market            = require('./market.js');
var bots               = require('./bot.js');


/* ORDER */
router.post('/api/order',               order.order);
router.get('/api/getAllOrder',          order.getAllOrder);

/* WALLET */
router.post('/api/createWallet',        wallet.createWallet);
router.get('/api/getWallet',            wallet.getWallet);
router.get('/api/getAllWallet',         wallet.getAllWallet);
router.post('/api/rebalance',           wallet.rebalance);

/* RUNNING BOTS */
router.get('/api/bot/getAll',           bots.getAllRunning);
router.get('/api/bot/getSingle',        bots.getRunning);
router.post('/api/bot/add',             bots.addBot);
router.post('/api/bot/remove',          bots.removeBot);

/* ICHIMOKU */
router.post('/api/ichimoku/script',     ichimoku.ichimoku);
router.post('/api/ichimoku/start',      ichimoku.startichimoku);
router.post('/api/ichimoku/stop',       ichimoku.stop);

/* MACD */
router.post('/api/macd/script',         macd.macd);
router.post('/api/macd/start',          macd.startmacd);
router.post('/api/macd/stop',           macd.stop);

/* RSI */
router.post('/api/rsi/script',          rsi.rsi);
router.post('/api/rsi/start',           rsi.startrsi);
router.post('/api/rsi/stop',            rsi.stop);

/* MARKET */
router.get('/api/market',               market.market);



module.exports = router;
