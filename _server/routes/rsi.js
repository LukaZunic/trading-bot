var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var rsi = {
    rsi: (req,res,next) => {
        const {spawn} = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly'] 
        const childPython = spawn('py',['./scripts/rsi.py',req.body.id_rsi,req.body.name,req.body.start_date]);
        
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        childPython.stdout.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}` );
        });
        res.json({ message: 'RSI called'})
    },        
    startrsi: (req,res,next) => {
        var id_rsi = req.body.id_rsi;
        var name_rsi = req.body.name;
        var date_rsi = req.body.start_date;

        setInterval(()=>{
            var xhttp1 = new XMLHttpRequest();
            xhttp1.open("POST", "http://localhost:3014/api/rsi/script");
            xhttp1.setRequestHeader("Content-Type", "application/json")
            xhttp1.send(JSON.stringify({"id_rsi":id_rsi,"name":name_rsi,"start_date":date_rsi}));
        },1000);
        res.json()
    }
};

module.exports = rsi;