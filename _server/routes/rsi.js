var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var intervals = {};
var rsi = {
    stop: (req, res, next) => {
        clearInterval(intervals[req.body.id_rsi]);
        res.json({ message: `RSI ${req.body.id_rsi} bot terminated`})
        console.log('RSI bot terminated');
    },
    rsi: (req,res,next) => {
        const {spawn} = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly'] 
        const childPython = spawn('py',['./scripts/rsi.py',req.body.id_rsi,req.body.name,req.body.start_date, req.body.stop_loss, req.body.take_profit]);
        
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
            if(data.toString('utf-8').includes("TERMINATE TRADING BOT")){
                clearInterval(intervals[req.body.id_rsi]);
                console.log('RSI bot terminated');
            }
        });
        childPython.stdout.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}` );
        });
        res.json({ message: `RSI script called at ID: ${req.body.id_rsi}`})
    },        
    startrsi: (req,res,next) => {
        var id_rsi = req.body.id_rsi;
        var name_rsi = req.body.name;
        var date_rsi = req.body.start_date;
        var stop_loss=req.body.stop_loss;
        var take_profit=req.body.take_profit;
        intervals[req.body.id_rsi] = setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/rsi/script");
            xhttp1.setRequestHeader('Accept', 'application/json');
            xhttp1.setRequestHeader("Content-Type", "application/json")
            xhttp1.send(JSON.stringify({"id_rsi":id_rsi,"name":name_rsi,"start_date":date_rsi, "stop_loss": stop_loss, "take_profit": take_profit}));
        },5000);
        res.json({message: `RSI bot running at ID: ${req.body.id_rsi}`})
    }
};

module.exports = rsi;