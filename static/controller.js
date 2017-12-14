const table = $("#main-table");
const color = "#ffffcc";
var submitted_word;

var gameid = $("#game-id").text().substr(9);

var pingerId = setInterval(ping, 1000);

function ping(){
   $.ajax({
      url: '/ping/' + gameid,
      success: function(result){
        //  alert('reply');
      },
      error: function(result){
          // alert('timeout/error');
          clearInterval(pingerId);

      }
   });
};

$(".start-game-button").on('click', function(){
    $.ajax({url: "/randomletters/64", success: function(result){
        result = JSON.parse(result);
        var table = document.getElementById('main-table');
        var rowLength = table.rows.length;

        for(var i=0; i<rowLength; i+=1){
          var row = table.rows[i];

          //your code goes here, looping over every row.
          //cells are accessed as easy

          var cellLength = row.cells.length;
          for(var y=0; y<cellLength; y+=1){
            var cell = row.cells[y];
            cell.innerHTML = result[0];
            result.shift();
          }
        }

    }});
    $(this).css('display', 'none');

    // <form class="form-inline"><input type="text" class="form-control" id="current-word" value="" readonly></form>

    $('#current-word-row').append('<form class="form-inline"><input type="text" class="form-control" id="current-word" value="" readonly></form>');
    $('#button-row').append('<button type="submit" class="btn btn-default game-button" id="submit-word">submit word</button>');
    $('#button-row').append('<button type="submit" class="btn btn-default game-button" id="cancel-word">cancel word</button>');

    startgame();
});


var startgame = function () {
    // alert("Game started");
    const submit_button = $("#submit-word");
    const cancel_button = $("#cancel-word");
    var selected_word = "";
    var lastClicked = {"row": -1, "col": -1};
    var $prevClicked;

    var timeLeft = 30;
    var elem = document.getElementById('timer');
    elem.innerHTML = timeLeft + ' seconds remaining';

    var timerId = setInterval(countdown, 1000);

    function countdown() {
      if (timeLeft == 0) {
        clearTimeout(timerId);
        // endGame()????
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
      submitted_word = $("#current-word").val(selected_word);


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



}
