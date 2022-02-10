import logo from "./nabla.svg";
import "./Playground.css";
import { useEffect, useState } from "react";
import { GameState, initialState, Key, screenState, tick } from "../game";
import { GAME_OVER_SCREEN_STATE } from "./gameover";

const DELAY = 50;

function Playground() {
  const [lastKeyPressed, setLastKeyPressed] = useState(Key.Right);
  const [currentGameState, setCurrentGameState] = useState<
    GameState | "GameOver"
  >(initialState());

  const onKeyDown = (key: string) => {
    switch (key) {
      case "ArrowUp":
        setLastKeyPressed(Key.Up);
        break;
      case "ArrowDown":
        setLastKeyPressed(Key.Down);
        break;
      case "ArrowLeft":
        setLastKeyPressed(Key.Left);
        break;
      case "ArrowRight":
        setLastKeyPressed(Key.Right);
        break;
    }
  };

  useInterval(DELAY, () => {
    if (currentGameState == "GameOver") return;
    setCurrentGameState(tick(currentGameState, lastKeyPressed));
  });

  return (
    <div className="App" tabIndex={0} onKeyDown={(e) => onKeyDown(e.key)}>
      <img src={logo} className="Logo" alt="Nabla" />
      <div className="Game">
        {(currentGameState == "GameOver"
          ? GAME_OVER_SCREEN_STATE
          : screenState(currentGameState)
        ).map((color, i) => (
          <div key={i} style={{ backgroundColor: color }} />
        ))}
      </div>
    </div>
  );
}

const useInterval = (delay: number, handler: TimerHandler) => {
  useEffect(() => {
    const interval = setInterval(handler, delay);
    return () => clearInterval(interval);
  });
};

export default Playground;
