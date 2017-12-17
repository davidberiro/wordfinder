// alert("hellooooo");

$("#join-game-button").on('click', function(){
  event.preventDefault();
  // alert("clicked");
  var username = $("#join-game-username").val();
  var gameid = $("#game-id-form").val();

  // $.ajax({
  //   type: "POST",
  //   url: "{{ url_for('joingame') }}",
  //   contentType: "application/json; charset=utf-8",
  //   data: {username: username, gameid: gameid},
  //   error: function(result){
  //     alert("error, probably no game with that id");
  //   }
  // })
  $.post("/joingame", {username: username, gameid: gameid}, function(response)
  {
      $("#main-container").html(response);
    }
  )
});

$("#create-game-button").on('click', function(){
  event.preventDefault();
  // alert("clicked");
  var username = $("#create-game-username").val();

  $.ajax({
    type: "POST",
    url: "/creategame",
    contentType: "application/json; charset=utf-8",
    data: {username: username},
    success: function(result){
      $("#main-container").html(result);
    },
    error: function(result){
      alert("error, probably no game with that id");
    }
  });
  // $.post("/creategame/", {username: username}, function(response)
  // {
  //     $("#main-container").html(response);
  //   }
  // )
});
