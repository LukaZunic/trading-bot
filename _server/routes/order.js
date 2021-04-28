var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');

var order = {
    order: (req, res, next) => {
        try{

            if(req.body.timestamp && req.body.type && req.body.name && req.body.quantity && req.body.price && req.body.method){
                let order_details = [
                    req.body.timestamp,
                    req.body.type,
                    req.body.name,
                    req.body.quantity,
                    req.body.price,
                    req.body.method
                ]
                let query = "INSERT INTO `tradingbot`.`order` (`timestamp`, `type`, `name`, `quantity`, `price`, `method`) VALUES (?);";
                let table = [order_details];
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

module.exports = order;