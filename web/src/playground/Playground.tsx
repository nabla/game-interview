import logo from "./nabla.svg";
import "./Playground.css";
import { useEffect, useState } from "react";
import { Color, GameState, HEIGHT, initialState, Key, draw, tick, WIDTH } from "../game";
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
    const newGameState = tick(currentGameState, lastKeyPressed);
    // Re-render even if the `tick` mutated the current state instead of returning a new one.
    setCurrentGameState(newGameState === "GameOver" ? newGameState : {...newGameState});
  });

  let pixels: Color[];
  if (currentGameState == "GameOver") {
    pixels = GAME_OVER_SCREEN_STATE;
  } else {
    pixels = Array(WIDTH * HEIGHT).fill(Color.Black);
    draw(currentGameState, (x, y, color) => {
      pixels[(x % WIDTH) + (y * WIDTH)] = color;
    });
  }

  useEffect(() => {
    const gameZone = document.getElementById("game-zone");
    gameZone?.focus();
  }, []);

  return (
    <div className="App" tabIndex={0} onKeyDown={(e) => onKeyDown(e.key)} id="game-zone">
      <img src={logo} className="Logo" alt="Nabla" />
      <div className="Game">
        {pixels.map((color, i) => (
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
