// CODE FOR XML REQUESTS - COURTESY OF PROF TIM JAMES THE REAL MVP OF PITT CS
function createXmlHttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }
    if (!(xmlhttp)) {
        alert("Your browser does not support AJAX!");
    }
    return xmlhttp;
}

// this function converts a simple key-value object to a parameter string.
function objectToParameters(obj) {
    var text = '';
    for (var i in obj) {
        // encodeURIComponent is a built-in function that escapes to URL-safe values
        text += encodeURIComponent(i) + '=' + encodeURIComponent(obj[i]) + '&';
    }
    return text;
}


function postParameters(xmlHttp, target, parameters) {
    if (xmlHttp) {
        xmlHttp.open("POST", target, true); // XMLHttpRequest.open(method, url, async)
        var contentType = "application/x-www-form-urlencoded";
        xmlHttp.setRequestHeader("Content-type", contentType);
        xmlHttp.send(parameters);
    }
}

function sendJsonRequest(parameterObject, targetUrl, callbackFunction) {
    var xmlHttp = createXmlHttp();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            var myObject = JSON.parse(xmlHttp.responseText);
            callbackFunction(myObject, targetUrl, parameterObject);
        }
    }
    postParameters(xmlHttp, targetUrl, objectToParameters(parameterObject));
}

function get(xmlHttp, target) {
    if (xmlHttp) {
        xmlHttp.open("GET", target, true); // XMLHttpRequest.open(method, url, async)
        var contentType = "application/x-www-form-urlencoded";
        xmlHttp.setRequestHeader("Content-type", contentType);
        xmlHttp.send();
    }
}

function sendGetRequest(targetUrl, callbackFunction) {
    var xmlHttp = createXmlHttp();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            var myObject = JSON.parse(xmlHttp.responseText);
            callbackFunction(myObject, targetUrl);
        }
    }
    get(xmlHttp, targetUrl)
}

function getData(targetUrl, callbackFunction) {
    let xmlHttp = createXmlHttp();
    xmlHttp.onreadystatechange = function() {
        if (xmlHttp.readyState == 4) {
            // note that you can check xmlHttp.status here for the HTTP response code
            try {
                let myObject = JSON.parse(xmlHttp.responseText);
                callbackFunction(myObject, targetUrl);
            } catch (exc) {
                console.log("There was a problem at the server.");
            }
        }
    }
    xmlHttp.open("GET", targetUrl, true);
    xmlHttp.send();
}

var fake_son = {}
function fake_callback() {}

function create_game() {
    console.log('GOING TO CREATE GAME SCREEN');
    //sendJsonRequest(fake_son, '/create_game', fake_callback)
    location.href = 'create_game.html';
}

// Start a game that has been created on the create game screen
function start_game() {
    var username = document.getElementById('game_name').value;
    var game_name = username + "'s Game";
    var game_json = {
        "Hostname" : username,
        "GameName" : game_name
    }
    sendJsonRequest(game_json, '/start_game', send_to_game)
}

var username  = ""
// Function to send the user to the game screen
function send_to_game(data) {
    username = data['hostName']
    window.location.href = 'main_game.html';
}

function get_session_data() {
    sendJsonRequest(fake_son, '/get_session_data', setup_game_screen)
}
function setup_game_screen(data) {
    document.title = data['username'] + "'s Game"
    document.getElementById('game_name_title').innerText = data['username'] + "'s Game"
    document.getElementById('game_code_data').innerText = data['game_code']
    // Check to see if they created the game

    // Else check the database for the game to populate the areas

    // Change page title

    // populate the player area

}
// Function to populate the player area
function get_players(game_code) {
    var json_req = {
        "game_code" : game_code
    }
    sendJsonRequest(json_req, '/populate_players', populate_player_area)
}

function populate_player_area(player_data) {
    console.log(player_data);
}

function join_game() {
    var game_code = document.getElementById('game_code').value;
    if ((game_code.length == 0)) {
        console.log('NO CODE ENTERED');
        return;
    }
    // Send the code to the backend
    console.log(game_code);
}

