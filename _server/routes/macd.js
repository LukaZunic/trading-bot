var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;


var intervals = {};
var macd = {
    stop: (req, res, next) => {
        clearInterval(intervals[req.body.id_macd]);
        res.json({ message: `MACD ${req.body.id_macd} bot terminated`})
        console.log('MACD bot terminated');
    },
    macd: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/macd.py',req.body.id_macd,req.body.name,req.body.start_date, req.body.stop_loss, req.body.take_profit]);
        
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
            if(data.toString('utf-8').includes("TERMINATE TRADING BOT")){
                clearInterval(intervals[req.body.id_macd]);
                console.log('MACD bot terminated');
            }
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
        });
        res.json({ message: `MACD script called at ID: ${req.body.id_macd}`});
    },
    
    startmacd: (req, res, next) => {
        var id_macd = req.body.id_macd;
        var name_macd=req.body.name;
        var date_macd=req.body.start_date;
        var stop_loss=req.body.stop_loss;
        var take_profit=req.body.take_profit;
        
        intervals[req.body.id_macd] = setInterval(()=>{
                var xhttp1 = new XMLHttpRequest();
                xhttp1.open("POST", "http://localhost:3014/api/macd/script");
                xhttp1.setRequestHeader('Accept', 'application/json');
                xhttp1.setRequestHeader("Content-Type", "application/json");
                xhttp1.send(JSON.stringify({"id_macd":id_macd, "name": name_macd, "start_date": date_macd, "stop_loss": stop_loss, "take_profit": take_profit}));
            },5000)
        res.json({message: `MACD bot running at ID: ${req.body.id_macd}`});
    }
};

module.exports = macd;