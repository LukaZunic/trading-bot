var express     = require('express');
var mysql       = require('mysql');
var bcrypt      = require('bcrypt');
var app         = express();
var http        = require('http');
var md5         = require('MD5');
var cors        = require('cors');
var bodyParser  = require('body-parser');
var apiToken    = require('api-token');
var connection  = require('./connection');
var functions   = require('./routes/functions.js');
var helmet      = require('helmet');
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;

var apiRoutes = express.Router();

apiToken.setExpirationTime(365); // 365 days valid token

var port = process.env.PORT || 3014; // used to create, sign, and verify tokens

app.use(helmet()) // secures express app

app.use(cors()); // cross-origin resource sharing

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); //json body-parser


app.all('/api/*', function(req, res, next){

    var token = (req.body && req.body.access_token) || (req.query && req.query.access_token) || req.headers['x-access-token'];
    console.log(req.body);
    
    if(req.get('token')){
        token = req.get('token');
    }
    else if (req.query.token){
        token = req.query.token;
    }
    //test
    else if(req.url.substring(0,5) === '/api/'){
        console.log('TESTNI API');
        next();
    }
    else if(apiToken.isTokenValid(token)){
        /* continue if token is valid */
         next();
    }else{
        /* send 401 if not authenticating or token is invalid */
        //res.send(401);
        //res.send("Authenticate");
         res.json({ success: false, message: 'Authentication failed. Invalid token. Login again!' });
    }

});

app.use('/', require('./routes'));

app.use('/api', apiRoutes);

app.get('/', function(req, res){
    res.json({ message: 'API'});
});

/* API CALL TO RUN SCRIPT */
app.post('/macd', function(req, res){
    const { spawn } = require('child_process');

    var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']

    const childPython = spawn('py', ['./scripts/macd.py',req.body.name,req.body.start_date]);
    
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
});

app.post('/ichimoku', function(req, res){
    const { spawn } = require('child_process');

    var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']

    const childPython = spawn('py', ['./scripts/ichimoku_cloud.py',req.body.name,req.body.start_date]);

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
});

app.post('/ichimokuBollinger', function(req, res){
    const { spawn } = require('child_process');

    var pip_prerequirments = ['-m pip install sys','-m pip install numpy','-m pip install pandas','-m pip install yfinance','-m pip install requests','-m pip install datetime', '-m pip install plotly']

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
});

/* API CALL TO START SCRIPT LOOP */

app.post('/startMACD', function(req, res){
    name_=req.body.name;
    date_=req.body.start_date;

    setInterval(()=>{
        var xhttp1 = new XMLHttpRequest();
        xhttp1.open("POST", "http://localhost:3014/macd");
        xhttp1.setRequestHeader("Content-Type", "application/json");
        xhttp1.send(JSON.stringify({ "name": name_, "start_date": date_}));
    },1000);
    
    res.json()
});

app.post('/startIchimoku', function(req, res){
    name_=req.body.name;
    date_=req.body.start_date;

    setInterval(()=>{
        var xhttp1 = new XMLHttpRequest();
        xhttp1.open("POST", "http://localhost:3014/ichimoku");
        xhttp1.setRequestHeader("Content-Type", "application/json");
        xhttp1.send(JSON.stringify({ "name": name_, "start_date": date_}));
    },1000);
    
    res.json()
});

app.post('/startIchiBoll', function(req, res){
    name_=req.body.name;
    date_=req.body.start_date;

    setInterval(()=>{
        var xhttp1 = new XMLHttpRequest();
        xhttp1.open("POST", "http://localhost:3014/ichimokuBollinger");
        xhttp1.setRequestHeader("Content-Type", "application/json");
        xhttp1.send(JSON.stringify({ "name": name_, "start_date": date_}));
    },1000);
    
    res.json()
});

connection.init();

app.listen(port);
console.log('Listening at http://localhost:' + port);