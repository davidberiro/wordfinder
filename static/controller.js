const table = $("#main-table");
const color = "#ffffcc";
var submitted_word;
var submitted_words = [];
var gameInfo = {"num_of_players": 1, "last_pinged": null, "p1_name": null, "p2_name": null, "game_started": "false", "crossword": null,
                "submitted_words": {"p1": [], "p2": []}};
var gameid = $("#game-id").text().substr(9);
var initializedGame = false
var pingForWordsId;
var pingerId = setInterval(ping, 1000);
var player_id;
var checked_player_id = false;

function tellServerGameStarted(){
  $.ajax({
    url: '/startgame/'+gameid,
    success: function(response){
      gameInfo = response;
    }
  })
};

function pingForSubmittedWords(){
  $.ajax({
    type: 'POST',
    url: 'pingforwords/'+gameid+'/'+player_id,
    data: JSON.stringify({"words": submitted_words}),
    contentType: 'application/json;charset=UTF-8',
    success: function(result){
      updateSubmittedWords(result["submitted_words"], gameInfo["submitted_words"]);
      gameInfo = result;
    },
    error: function(result){
      clearInterval(pingForWordsId);
    }
  })
};

function ping(){
   $.ajax({
      url: '/ping/' + gameid,
      success: function(result){
        gameInfo = result;
        if (!checked_player_id){
          if (gameInfo["num_of_players"] == 1){
            player_id = "p1";
          }
          else{
            player_id = "p2";
          }
          checked_player_id = true;
        }
        if (gameInfo["num_of_players"] == 2){
          $("#p2name").html(gameInfo["p2_name"]);
          $("#p2-words").html(gameInfo["p2_name"] + "'s words");
        }
        if (gameInfo["game_started"] == "true" && !initializedGame && gameInfo["crossword"] != null){
          initializedGame = true;
          startgame();
          clearInterval(pingerId);
          pingForWordsId = setInterval(pingForSubmittedWords, 1000);
        }
      },
      error: function(result){
          clearInterval(pingerId);
        }
   });
};

function appendWord(word, player){
  var id = "#"+player+"-table";
  $(id).append("<tr><td id="+player+word+">"+word+"</td></tr>");
}

function updateSubmittedWords(updated_words, old_words){
  p1_old_words = old_words["p1"];
  p2_old_words = old_words["p2"];
  p2_updated_words = updated_words["p2"];
  p1_updated_words = updated_words["p1"];

  if (p1_updated_words.length > p1_old_words.length){
    appendWord(p1_updated_words[p1_updated_words.length-1], "p1");
  }
  if (p2_updated_words.length > p2_old_words.length){
    appendWord(p2_updated_words[p2_updated_words.length-1], "p2");
  }
}

$(".start-game-button").on('click', function(){
    // initializedGame = true;
    if (gameInfo["num_of_players"] == 1){
      alert("You can't play the game all by yourself...");
      return;
    }
    $.ajax({
      url: "/randomletters/64/"+gameid,
      success: function(result){
        gameInfo = result;
      }

    });
    tellServerGameStarted();

    // startgame();
});

var initTable = function(table) {
  result = JSON.parse(table);
  var table = document.getElementById('main-table');
  var rowLength = table.rows.length;

  for(var i=0; i<rowLength; i+=1){
    var row = table.rows[i];

    var cellLength = row.cells.length;
    for(var y=0; y<cellLength; y+=1){
      var cell = row.cells[y];
      cell.innerHTML = result[0];
      result.shift();
    }
  }
};

var startgame = function () {

    $(".start-game-button").css('display', 'none');
    initTable(gameInfo["crossword"]);

    $('#current-word-row').append('<form class="form-inline"><input type="text" class="form-control" id="current-word" value="" readonly></form>');
    $('#button-row').append('<button type="submit" class="btn btn-default game-button" id="submit-word">submit word</button>');
    $('#button-row').append('<button type="submit" class="btn btn-default game-button" id="cancel-word">cancel word</button>');

    // alert("Game started");
    const submit_button = $("#submit-word");
    const cancel_button = $("#cancel-word");
    var selected_word = "";
    var lastClicked = {"row": -1, "col": -1};
    var $prevClicked;

    var timeLeft = 60;
    var elem = document.getElementById('timer');
    elem.innerHTML = timeLeft + ' seconds remaining';

    var timerId = setInterval(countdown, 1000);

    function countdown() {
      if (timeLeft == 0) {
        clearTimeout(timerId);
        $("#timer").html("");
        endgame()
      } else {
        elem.innerHTML = timeLeft + ' seconds remaining';
        timeLeft--;
      }
    }

    cancel_button.on('click', function(){
      table.find('td').css('background-color', 'white');
      selected_word = "";
      $("#current-word").val(selected_word);
      lastClicked.row = -1;
      lastClicked.col = -1;
    });

    submit_button.on('click', function(){
      submitted_word = $("#current-word").val();
      if (submitted_word == ""){
        return;
      }
      if ($.inArray(submitted_word, submitted_words) != -1){
        alert("Cannot submit same word twice");
        cancel_button.trigger('click');
        return;
      }
      submitted_words.push(submitted_word);
      cancel_button.trigger('click');
    });

    table.on('click', 'td', function(){
      // alert("clicked");
      var row = $(this).parent().attr('class');
      var col = $(this).attr('class');
      var row_number = parseInt(row[row.length - 1]);
      var col_number = parseInt(col[col.length - 1]);


      if (lastClicked.row == -1) {
        var selectedLetter = $(this).text();
        $(this).css('background-color', color);
        lastClicked.row = row_number;
        lastClicked.col = col_number;
        $prevClicked = $(this);
      }
      else if ((Math.abs((row_number - lastClicked.row)) <= 1) && (Math.abs((col_number - lastClicked.col)) <= 1)
          && ((row_number-lastClicked.row != 0) || (col_number-lastClicked.col != 0))) {
        $(this).css('background-color', color);
        $prevClicked.css('background-color', 'white');
        var selectedLetter = $(this).text();
        lastClicked.row = row_number;
        lastClicked.col = col_number;
        $prevClicked = $(this);
      }
      else {
        // alert user illegal next letter?
        return;
      }
      selected_word+=selectedLetter;
      $("#current-word").val(selected_word);
    });

  };

function endgame(){
  clearInterval(pingForWordsId);
  $.ajax({
    type: 'GET',
    url: 'endgame/'+gameid,
    success: function(response){
      display_score(response);
    }
  })
};

function display_score(results){
  p1_results = results["p1"]
  p2_results = results["p2"]
  p1_score = results["p1_points"]
  p2_score = results["p2_points"]
  for (var word in p1_results){
    $("#p1"+word).html(word + " " + p1_results[word] + " points");
  }
  for (var word in p2_results){
    $("#p2"+word).html(word + " " + p2_results[word] + " points");
  }
  if (p1_score == p2_score){
    alert("GAME IS A TIE!");
  }
  else{
    var winner = (p1_score > p2_score) ? gameInfo["p1_name"] : gameInfo["p2_name"];
    alert(winner + " WINS!");
  }
}

function checkword(word){
  $.get('checkword/'+word, function(response){
      var isword = (response["result"] == "true") ? true : false;
      alert(isword);
      return isword;
    });
  }
