var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var macdboll = {
    macdboll: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/macd_bollinger.py',req.body.id_macdboll,req.body.name,req.body.start_date]);
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
        });
        res.json({ message: 'MACD + BOLLINGER BANDS called'});
    },
    startmacdboll: (req, res, next) => {
        var id_macdboll = req.body.id_macdboll
        var name_macdboll=req.body.name;
        var date_macdboll=req.body.start_date;

        setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/macdboll/script");
            xhttp1.setRequestHeader("Content-Type", "application/json");
            xhttp1.send(JSON.stringify({"id_macdboll":id_macdboll, "name": name_macdboll, "start_date": date_macdboll}));
        },1000);

        res.json()
    }
};

module.exports = macdboll;