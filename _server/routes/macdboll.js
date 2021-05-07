var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var macdboll = {
    macdboll: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/ichimoku_bollinger.py',req.body.name,req.body.start_date]);
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
        });
        res.json({ message: 'ICHIMOKU + BOLLINGER BANDS called'});
    },
    startmacdboll: (req, res, next) => {
        name_=req.body.name;
        date_=req.body.start_date;

        setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/macdboll/script");
            xhttp1.setRequestHeader("Content-Type", "application/json");
            xhttp1.send(JSON.stringify({ "name": name_, "start_date": date_}));
        },1000);

        res.json()
    }
};

module.exports = macdboll;