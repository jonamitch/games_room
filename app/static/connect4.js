var player=1; //1 for Yellow / Human, 2 for Red / AI
var grid = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0]
];

function selectColumn(col) {
    var colstring = col.toString()
    $.get('/connect4/' + colstring
    ).done(function(response) {
        grid = response[0].grid
        if (player==1) {
            player=2;
            document.getElementById("colorTurn").innerHTML="AI (Red)";
        } else {
            player=1;
            document.getElementById("colorTurn").innerHTML="Human (Yellow)";
        }
        refreshGrid();
    }).fail(function() {
        document.getElementById("colorTurn").innerHTML="Error";
    });
}


//A function used to refresh the connect4 grid on screen
function refreshGrid() {
  for (var row = 0; row < 6; row++) {
    for (var col = 0; col < 7; col++) {
      if (grid[row][col]==0) {
                document.getElementById("cell"+row+col).style.backgroundColor="#FFFFFF";
      } else if (grid[row][col]==1) { //1 for yellow
                document.getElementById("cell"+row+col).style.backgroundColor="#FFFF00";
      } else if (grid[row][col]==2) { //1 for yellow
                document.getElementById("cell"+row+col).style.backgroundColor="#FF0000";
       }
    }
  }
}

//A function used to reset the connect4 grid on screen
function resetGrid() {
    grid = [
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0]
    ];
    player=1;
    document.getElementById("colorTurn").innerHTML="Human (Yellow)";
    refreshGrid();
}
