export const HEIGHT = 40;
export const WIDTH = 40;

/** Keys that the user can press. */
export enum Key {
  Up = "ArrowUp",
  Down = "ArrowDown",
  Left = "ArrowLeft",
  Right = "ArrowRight",
}

/** Possible colors for pixels on screen. */
export enum Color {
  Red = "red",
  White = "white",
  Black = "black",
}

/** Immutable representation of the state of the game. */
export type GameState = {
  x: number;
  y: number;
};

/** Creates an initial game state. */
export function initialState(): GameState {
  return { x: 0, y: 0 };
}

/** Produces the game state for the next tick. */
export function tick(
  currentState: GameState,
  lastKeyPressed: Key,
): GameState | "GameOver" {
  const { x, y } = currentState;
  let newState;

  switch (lastKeyPressed) {
    case Key.Up:
      newState = { x, y: y - 1 };
      break;
    case Key.Down:
      newState = { x, y: y + 1 };
      break;
    case Key.Left:
      newState = { x: x - 1, y };
      break;
    case Key.Right:
      newState = { x: x + 1, y };
      break;
  }

  if (
    newState.x < 0 ||
    newState.x >= WIDTH ||
    newState.y < 0 ||
    newState.y >= HEIGHT
  )
    return "GameOver";

  return newState;
}

/** Determines the color of each pixel on the screen. */
export function screenState(currentState: GameState): Array<Color> {
  return Array.from({ length: WIDTH * HEIGHT }, (_, index) => {
    const x = index % WIDTH;
    const y = Math.floor(index / HEIGHT);
    return y == currentState.y && x == currentState.x ? Color.Red : Color.Black;
  });
}
