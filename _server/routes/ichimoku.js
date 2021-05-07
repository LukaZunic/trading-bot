var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var ichimoku = {
    ichimoku: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/ichimoku_cloud.py',req.body.id_ichimoku,req.body.name,req.body.start_date]);
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
        });
        res.json({ message: 'ICHIMOKU called'});
    },
    startichimoku: (req, res, next) => {
        var id_ichimoku=req.body.id_ichimoku;
        var name_ichimoku=req.body.name;
        var date_ichimoku=req.body.start_date;
        setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/ichimoku/script");
            xhttp1.setRequestHeader("Content-Type", "application/json");
            xhttp1.send(JSON.stringify({"id_ichimoku":id_ichimoku, "name": name_ichimoku, "start_date": date_ichimoku}));
        },1000);
        res.json()
    }
};

module.exports = ichimoku;