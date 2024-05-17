import React, { useEffect, useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("There was an error fetching the data!", error);
      });
  }, []);

  const handleDrawCard = () => {
    axios
      .post("http://127.0.0.1:5000/draw", { move: "draw" })
      .then((response) => {
        setData(response.data.state);
        if (response.data.state.game_over) {
          console.log("Game Over:", response.data.state.winner);
        }
      })
      .catch((error) => {
        console.error("There was an error drawing a card!", error);
      });
  };

  const handleEndTurn = () => {
    axios
      .post("http://127.0.0.1:5000/ai_turn")
      .then((response) => {
        setData(response.data);
        if (response.data.game_over) {
          console.log("Game Over:", response.data.winner);
        }
      })
      .catch((error) => {
        console.error("There was an error ending the turn!", error);
      });
  };

  const handleNewRound = () => {
    axios
      .post("http://127.0.0.1:5000/reset")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("There was an error starting a new round!", error);
      });
  };

  const handleResetDeck = () => {
    axios
      .post("http://127.0.0.1:5000/reset_deck")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("There was an error resetting the deck!", error);
      });
  };

  const calculateHandValue = (hand) => {
    let value = 0;
    let numAces = 0;

    hand.forEach((card) => {
      const rank = card[0];
      if (rank === "Ace") {
        numAces += 1;
        value += 11;
      } else if (["Jack", "Queen", "King"].includes(rank)) {
        value += 10;
      } else {
        value += rank;
      }
    });

    // Adjust for aces
    while (value > 21 && numAces > 0) {
      value -= 10;
      numAces -= 1;
    }

    return value;
  };

  return (
    <div className="App">
      <header className="App-header">
        {data ? (
          <div>
            <p>
              Player Hand:{" "}
              {data.player_hand
                .map((card) => `${card[0]} of ${card[1]}`)
                .join(", ")}
            </p>
            <p>Player Total: {calculateHandValue(data.player_hand)}</p>
            <p>
              AI Hand:{" "}
              {data.ai_hand
                .map((card) => `${card[0]} of ${card[1]}`)
                .join(", ")}
            </p>
            <p>AI Total: {calculateHandValue(data.ai_hand)}</p>
            <p>Deck Count: {data.deck_count}</p>
            <p>Current Player: {data.current_player}</p>
            <p>Game Over: {data.game_over ? "Yes" : "No"}</p>
            <p>Winner: {data.winner}</p>
            <p>Player Score: {data.player_score}</p>
            <p>AI Score: {data.ai_score}</p>
            {data.current_player === "player" && !data.game_over && (
              <div>
                <button onClick={handleDrawCard}>Draw Card</button>
                <button onClick={handleEndTurn}>End Turn</button>
              </div>
            )}
            {data.game_over && (
              <div>
                <button onClick={handleNewRound}>Start New Round</button>
              </div>
            )}
          </div>
        ) : (
          <p>Loading...</p>
        )}
      </header>
    </div>
  );
}

export default App;
