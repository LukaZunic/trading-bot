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

connection.init();

app.listen(port);
console.log('Listening at http://localhost:' + port);