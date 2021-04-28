var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');

var wallet = {
    createWallet: (req, res, next) => {
        try{
            if(req.body.name && req.body.balance && req.body.method){
                let query = "INSERT INTO `tradingbot`.`wallet` (`name`, `quantity`, `balance`, `method`) VALUES (?, 0, ?, ?);";
                let table = [req.body.name, req.body.balance, req.body.method];
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
            if(req.body.method){
                let query = "SELECT * FROM `tradingbot`.`wallet` WHERE `method`=?";
                let table = [req.body.method];
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
    rebalance: (req, res, next) => {
        try{
            if(req.body.rebalance && req.body.quantity && req.body.method){
                let query = "UPDATE `tradingbot`.`wallet` SET `balance`= ?, `quantity`=? WHERE `method`=?";
                let table = [req.body.rebalance, req.body.quantity, req.body.method];
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