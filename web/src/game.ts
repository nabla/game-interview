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

/** Colors each pixel on the screen depending on the game state. */
export function draw(
  currentState: GameState,
  setColor: (x: number, y: number, color: Color) => void,
) {}
