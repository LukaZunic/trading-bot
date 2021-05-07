var mysql       = require('mysql');
var apiToken    = require('api-token');
var pool        = require('../connection');
var functions    = require('./functions.js');

function read_csv(path){
    //path = path.replace(/\\/g, '\\\\');
    const csvFilePath=path;
    //console.log(path)
    const csv=require('csvtojson');
    var ret = [];
    csv()
    .fromFile(csvFilePath)
    .then((jsonObj)=>{
        //console.log(jsonObj);
        ret.push(jsonObj);
    });
    return ret;
}
var market = {
    market: (req, res , next) => {
        const { spawn } = require('child_process');
        //var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']
        const childPython = spawn('py', ['./scripts/market.py']);
        childPython.stdout.on('data', (data) => {
            console.log(`stdout: ${data}`);
        });
        childPython.stderr.on('data', (data) => {
            console.log(`stderr: ${data}`);
        });
        childPython.on('close', (code) => {
            let path = __dirname;
            path = path.replace('routes', "scripts\\data\\")
            path = path.replace(/\\/g, '\\\\');
            var btc = read_csv(path + 'BTC-USD.csv');
            var eth = read_csv(path + 'ETH-USD.csv');
            var xrp = read_csv(path + 'XRP-USD.csv');
            var doge = read_csv(path + 'DOGE-USD.csv');
            var bch = read_csv(path + 'BCH-USD.csv');
            setTimeout(()=>{
                res.json({ message: 'Market data recieved.', btc_data: btc[0], eth_data: eth[0], xrp_data: xrp[0], doge_data: doge[0], bch_data: bch[0]}); //, eth_data: eth[0], xrp_data: xrp[0], doge_data: doge[0], bch_data: bch[0]
                console.log(`child process exited with code: ${code}`);
            },1000)
            
        });
        
    }
};

module.exports = market;