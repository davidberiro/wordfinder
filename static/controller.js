
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

    $('#button-row').append('<button type="submit" class="btn btn-default start-game-button">submit word</button>');
    $('#button-row').append('<button type="submit" class="btn btn-default start-game-button">cancel word</button>');

    startgame();
});


var startgame = function () {
    var timeLeft = 30;
    var elem = document.getElementById('timer');

    var timerId = setInterval(countdown, 1000);

    function countdown() {
      if (timeLeft == 0) {
        clearTimeout(timerId);
        // doSomething();
      } else {
        elem.innerHTML = timeLeft + ' seconds remaining';
        timeLeft--;
      }
    }
}
