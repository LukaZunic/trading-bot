var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var macd = {
    macd: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/macd.py',req.body.id_macd,req.body.name,req.body.start_date]);
        
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
        });
        res.json({ message: 'MACD called'});
    },
    startmacd: (req, res, next) => {
        var id_macd = req.body.id_macd;
        var name_macd=req.body.name;
        var date_macd=req.body.start_date;

        setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/macd/script");
            xhttp1.setRequestHeader("Content-Type", "application/json");
            xhttp1.send(JSON.stringify({"id_macd":id_macd, "name": name_macd, "start_date": date_macd}));
        },1000);

        res.json({message: 'MACD bot running'});
    }
};

module.exports = macd;