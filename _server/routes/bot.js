var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');

var bots = {
    addBot: (req, res, next) => {
        try{
            if(req.body.wallet_id){
                let botss = [
                    req.body.wallet_id
                ]
                let query = "INSERT INTO `tradingbot`.`running_bots` (`wallet_id`) VALUES (?);";
                let table = [botss];
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
    removeBot: (req, res, next) => {
        try{
            if(req.body.wallet_id){
                let botss = [
                    req.body.wallet_id
                ]
                let query = "DELETE FROM `tradingbot`.`running_bots` WHERE `wallet_id` = ?;";
                let table = [botss];
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
    getAllRunning: (req, res, next) => { 
        try{
            let query = "SELECT * FROM `tradingbot`.`running_bots`";            
            functions.mysql_queryV2(query,(dataSent)=>{
                functions.sendRes(res, dataSent);
            });
        }catch(err){
            console.log(err);
            functions.sendRes(res,{ success: false, message: 'Error, please check the passed data.', status: 503, data:err});
        }
    },
    getRunning: (req, res, next) => { 
        try{
            if(req.body.wallet_id){
                let botss = [
                    req.body.wallet_id
                ]
                let query = "SELECT * FROM `tradingbot`.`running_bots` WHERE `wallet_id` = ?;";
                let table = [botss];
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

module.exports = bots;
