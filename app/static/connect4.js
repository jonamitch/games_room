var player=1; //1 for Yellow / Human, 2 for Red / AI
var grid = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0]
];
var winner = null;
var lock = null;

function selectColumn(col) {
    colString = col.toString()
    console.log(lock);
    if (!winner && !lock) {
        lock = true;
        console.log(lock);
        request_human = {"entryCol": colString, "grid": JSON.stringify(grid), "player": player}
        $.post('/connect4/entryCol', request_human).done(function(response_human) {
            updateForResponse(response_human)
            if (!winner) {
                request_ai = {"grid": JSON.stringify(grid), "player": player}
                $.post('/connect4/entryCol', request_ai).done(function(response_ai) {
                    updateForResponse(response_ai)
                    lock = null;
                }).fail(function() {
                    document.getElementById("colorTurn").innerHTML="Error";
                });
            }
        }).fail(function() {
            document.getElementById("colorTurn").innerHTML="Error";
        });
    }
}

function updateForResponse(response) {
    grid = response[0].grid;
    winner = response[0].winner;
    position = response[0].position;
    refreshGrid();
    if (winner) {
        document.getElementById("colorTurn").innerHTML="We have a winner! Player: " + player.toString();
    } else if (player==1 && position) {
        player=2;
        document.getElementById("colorTurn").innerHTML="AI player 2 (Red)"
    } else if (position) {
        player=1;
        document.getElementById("colorTurn").innerHTML="Human player 1 (Yellow)";
    }
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
    winner = null;
    refreshGrid();
}
