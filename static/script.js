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
    location.href = 'main_game.html';
}

function get_session_data() {
    sendJsonRequest(fake_son, '/get_session_data', setup_game_screen)
}
function setup_game_screen(data) {
    document.title = data['username'] + "'s Game"
    document.getElementById('game_name_title').innerText = data['host_name'] + "'s Game"
    document.getElementById('game_code_data').innerText = data['game_code']
    // Check to see if they created the game
    // populate the player area
    get_players(data['game_code']);
}
// Function to populate the player area
function get_players(game_code) {
    var json_req = {
        "game_code" : game_code
    }
    sendJsonRequest(json_req, '/populate_players', populate_player_area)
}

function populate_player_area(player_data) {
    populate_player_area_loop(player_data.players[0]);
    get_current_card();
}
function populate_player_area_loop(player_list) {
    for (var i = 0; i < player_list.length; i++) {
        // Populate the player list in the right column
        var player_name_div = document.createElement("div");
        player_name_div.className = "player_card";
        player_name_div.id = player_list[i] + "_btn";
        player_name_div.setAttribute('onclick', "view_cards('" + player_list[i] + "')")
        //player_name_div.setAttribute('data-toggle', "modal")
        //player_name_div.setAttribute('data-target', "#myModal")
        var player_name_text = document.createElement('H5');
        player_name_text.innerText = player_list[i];
        player_name_div.appendChild(player_name_text);
        document.getElementById('players_div_area').appendChild(player_name_div);

        // Populate the dropdown
        var divider = document.createElement('li');
        divider.className = 'divider';
        var dropdown_selection = document.createElement("li");
        dropdown_selection.setAttribute("onclick", "set_vote('" + player_list[i] + "')");
        dropdown_selection.className = "player_choice";
        dropdown_selection.innerText = player_list[i];
        var dropdown_selection_div = document.getElementById('dropdown_choices');
        dropdown_selection_div.appendChild(dropdown_selection);
        dropdown_selection_div.appendChild(divider);
    }
}

function get_new_card() {
    sendJsonRequest(fake_son, '/get_new_card', update_card);
}

function get_current_card(game_code) {
    var json_data = {
        'game_code': game_code
    }
    sendJsonRequest(json_data, '/get_current_card', update_card);
}

function update_card(card_data) {
    document.getElementById('card_data').innerText = card_data['current_card'];
}

// Function that will update all UI elements that need to continually be updated
function update_UI() {
    sendJsonRequest(fake_son, '/get_UI_info', update_UI_callback)
}

function update_UI_callback(session_data) {
    // Update the current card
    update_card(session_data['current_card']);
    // Update the number of players
    populate_player_area_loop(session_data['players']);
}

function join_game() {
    var game_code = document.getElementById('game_code').value;
    if ((game_code.length == 0)) {
        console.log('NO CODE ENTERED');
        return;
    }
    // Send the code to the backend
    console.log(game_code);
    var username = prompt("Please Enter a Username");
    if ((username.length == 0)) {
        console.log('NO CODE ENTERED');
        alert('Username is not valid, please retry')
        return;
    }
    var join_data = {
        'username': username,
        'game_code': game_code
    }
    sendJsonRequest(join_data, '/user_join_attempt', finished_join)
}

// Callback for after a player has attempted to join a game
function finished_join(data) {
    console.log(data)
    if (data['Success'] == "True") {
        console.log('Successfully found game and entered user')

        location.href = 'main_game.html';
    } else {
        if (data['Error'] == 'Username Already Taken') {
            alert('Username has already been taken, please select another');
        } else if (data['Error'] == 'Game Does Not Exist') {
            alert('There is no active game matching your code, please try again');
        }
    }
}

function cast_vote() {
    // Get the text from the dropdown to submit as the vote
    vote = document.getElementById('selected_choice').innerText;
    console.log('User voted for: ' + vote);
    var json_sent = {
        "choice": vote
    }
    sendJsonRequest(json_sent, '/cast_vote', update_UI)
}

function set_vote(vote_username) {
    // Change the dropdown text to be their current vote
    console.log(vote_username);
    document.getElementById('selected_choice').innerText = vote_username;
}

function view_cards(player_name) {
    console.log('Attempting to view cards for player: ' + player_name);
    var json_req = {
        'player_name': player_name
    }
    sendJsonRequest(json_req, '/get_players_cards', view_player_cards)
}

function view_player_cards(data) {
    cards_list = data['cards_won'];
    player_name = data['selected_player']
    console.log(player_name)
    $('#modal_player_name').text(player_name + "'s Cards Won");
    if (cards_list.length != 0) {
        for(var i = 0; i < cards_list.length; i++) {
            $('#modal_area').append("<h4>" + cards_list[i] +"</h4>")
        }
    } else {
        $('#modal_area').append("<h4> None :( </h4>")
    }
    $('#myModal').modal('show');
    //update_UI();
}

function tally_votes() {
    console.log('tallying the votes');
    // TODO - CALL ENDPOINT THAT WILL TALLY VOTES -> ALERT THE WINNER?
}
// TODO - WRITE A FUNCTION TO CONTINUALLY UPDATE THE UI SO THAT PLAYERS SEE VOTES, NEW CARDS, ETC
