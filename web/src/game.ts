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
export type GameState = {};

/** Creates an initial game state. */
export function initialState(): GameState {
  return {};
}

/** Produces the game state for the next tick. */
export function tick(
  currentState: GameState,
  lastKeyPressed: Key,
): GameState | "GameOver" {
  return {};
}

/** Determines the color of each pixel on the screen. */
export function screenState(currentState: GameState): Array<Color> {
  return Array.from({ length: WIDTH * HEIGHT }, (_, index) => {
    const x = index % WIDTH;
    const y = Math.floor(index / HEIGHT);
    return Color.Black;
  });
}
