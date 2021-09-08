var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
var intervals = {};
var ichimoku = {
    stop: (req, res, next) => {
        clearInterval(intervals[req.body.wallet_id]);
        res.json({ message: `ICHIMOKU CLOUD ${req.body.wallet_id} bot terminated`})
        console.log('ICHIMOKU CLOUD bot terminated');
    },
    ichimoku: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/ichimoku_cloud.py',req.body.id_ichimoku,req.body.name,req.body.start_date, req.body.stop_loss, req.body.take_profit]);
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
            if(data.toString('utf-8').includes("TERMINATE TRADING BOT")){
                clearInterval(intervals[req.body.id_ichimoku]);
                console.log('ICHIMOKU CLOUD bot terminated');
            }
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
        });
        res.json({ message: `ICHIMOKU CLOUD script called at ID: ${req.body.id_ichimoku}`});
    },
    startichimoku: (req, res, next) => {
        var id_ichimoku=req.body.wallet_id;
        var name_ichimoku=req.body.name;
        var date_ichimoku=req.body.start_date;
        var stop_loss=req.body.stop_loss;
        var take_profit=req.body.take_profit;
        intervals[req.body.wallet_id] = setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/ichimoku/script");
            xhttp1.setRequestHeader('Accept', 'application/json');
            xhttp1.setRequestHeader("Content-Type", "application/json");
            xhttp1.send(JSON.stringify({"id_ichimoku":id_ichimoku, "name": name_ichimoku, "start_date": date_ichimoku, "stop_loss": stop_loss, "take_profit": take_profit}));
        },5000);
        res.json({message: `ICHIMOKU CLOUD bot running at ID: ${req.body.wallet_id}`})
    }
};

module.exports = ichimoku;