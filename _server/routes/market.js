var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');

var market = {
    market: (req, res , next) => {
        const { spawn } = require('child_process');
        var datas;
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/market.py']);
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data.toString()}`);
            //console.log(typeof(data))
            //console.log(Object.entries(data));
            datas=Buffer.from(JSON.stringify(data));
            datas = JSON.parse(datas.toString());
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            console.log(`child process exited with code: ${code}`);
            res.json({ message: 'Market data recieved.', datas: datas});
        });
        
    }
};

module.exports = market;