var mysql = require('mysql');

var apiToken = require('api-token');

var pool = require('../connection');

var fs = require('fs');

var functions = {

sendRes: function(res, data){
    res.json({ success: data.success, message: data.message, status: data.status, data:data.data});
    return 1;
},

mysql_query:function(upit, callback){
    //console.log(upit);
    function funkcija1(a, callback){
        
        pool.getConnection(function(err, connection){
            if(err) {
                //connection.release();
                callback(500, err);
            }else{
                connection.query(a,function(err, rows) {
                    connection.release();
                    if(err){
                        console.log(err);
                        callback(501, err);
                    }else{
                        callback(true, rows);
                    }                          
                });
            }
        });
    }

    try{
        if(typeof(upit)==='string'){
            funkcija1(upit, function(rezultat, podaci){
                if(rezultat == true){
                    callback({ success: true, message: 'Successful', status: rezultat, data:podaci });
                }else{
                    callback({ success: false, message: 'Database or connection error', status: rezultat, data:podaci });
                }
            });
        }else{
            callback({ success: false, message: 'Query is not sent in valid form!', status: 502, data:[] });
        }
    }catch(err){
        console.log(err);
        callback({ success: false, message: 'Error, please check the sent data!', status: 503, data:err });
    }
},

mysql_queryV2:function(_query, callback){
    function function1(a, callback){
        
        pool.getConnection(function(err, connection){
            if(err) {
                callback(500, err, 'Connection error!');
            }else{
                connection.query(a,function(err, rows) {
                    connection.release();
                    if(err){
                        callback(501, err, 'Query error');
                    }else{
                        try {
                            if(typeof(rows) == "object"){
                                if(rows.length > 0){
                                    if(rows[0][0]){
                                        //PROCEDURE
                                        callback(true, rows[0], 'Data exists!');
                                    }else{
                                        callback(true, rows, 'Data exists!');
                                    }  
                                }else{
                                    if(rows.insertId >= 0){
                                        //PROCEDURE bez returna i UPDATE, DELETE, INSERT
                                        callback(true, rows,'Successful');
                                    }else{
                                        callback(false, rows,'Data does not exist!');
                                    }
                                }
                            }else{
                                callback(false, rows,'Data does not exist!');
                            }
                        } catch (error) {
                            callback(false, error,'Error while fetching data!');
                        }
                    }                          
                });
            }
        });
    }

    try{
        if(typeof(_query)==='string'){
            function1(_query, function(success, data, message){
                if(success == true){
                    callback({ success: true, message: message, status: success, data:data });
                }else{
                    callback({ success: false, message: message, status: success, data:data });
                }
            });
        }else{
            callback({ success: false, message: 'Query is not sent in valid form!', status: 502, data:[] });
        }
    }catch(err){
        console.log(err);
        callback({ success: false, message: 'Error, please check the sent data!', status: 503, data:err });
    }
},
err_data: { success: false, message: 'Error, please check the sent data!', status: 502, data:[] },
err_validation: function(data){
    //let a= JSON.stringify(err);
    return {success: false, message: 'Validation error', status: 504, data:data}
},
err_custom: function(success, message, status, data){
    //let a= JSON.stringify(err);
    return {success: success, message: message, status: status, data:data}
},
err_unknown: function(err){
    console.log(err);
    //let a= JSON.stringify(err);
    return {success: false, message: 'Error, please check the sent data!', status: 503, data:err}
}

};



module.exports = functions;