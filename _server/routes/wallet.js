var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');

var wallet = {
    createWallet: (req, res, next) => {
        try{
            if(req.body.wallet_id && req.body.name && req.body.balance && req.body.method){
                //let r = Math.random().toString(36).substring(7);
                let query = "INSERT INTO `tradingbot`.`wallet` (`id`, `name`, `quantity`, `balance`, `method`) VALUES (?, ?, 0, ?, ?);";
                let table = [req.body.wallet_id, req.body.name, req.body.balance, req.body.method];
                query = mysql.format(query, table);
                functions.mysql_queryV2(query, function(dataSent){
                    functions.sendRes(res, dataSent);
                });
                
            }else{
                functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.!', status: 502, data:[]});
            }
        }catch(err){
            console.log(err);
            functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.', status: 503, data:err});
        }
    },
    getWallet: (req, res, next) => { 
        try{
            if(req.body.id && req.body.method){
                let query = "SELECT * FROM `tradingbot`.`wallet` WHERE `id`=? AND `method`=?";
                let table = [req.body.id,req.body.method];
                query = mysql.format(query, table);
                functions.mysql_queryV2(query, function(dataSent){
                    functions.sendRes(res, dataSent);
                });
            }else{
                functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.!', status: 502, data:[]});
            }
        }catch(err){
            console.log(err);
            functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.', status: 503, data:err});
        }
    },
    getAllWallet: (req, res, next) => { 
        try{
            let query = "SELECT * FROM `tradingbot`.`wallet`";            
            functions.mysql_queryV2(query,(dataSent)=>{
                functions.sendRes(res, dataSent);
            });
        }catch(err){
            console.log(err);
            functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.', status: 503, data:err});
        }
    },
    rebalance: (req, res, next) => {
        try{
            if(req.body.id && req.body.rebalance && req.body.quantity && req.body.method){
                let query = "UPDATE `tradingbot`.`wallet` SET `balance`= ?, `quantity`=? WHERE `method`=? and `id`=?";
                let table = [req.body.rebalance, req.body.quantity, req.body.method, req.body.id];
                query = mysql.format(query, table);
                functions.mysql_queryV2(query, function(dataSent){
                    functions.sendRes(res, dataSent);
                });
            }else{
                functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.!', status: 502, data:[]});
            }
        }catch(err){
            console.log(err);
            functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.', status: 503, data:err});
        }
    }
};

module.exports = wallet;