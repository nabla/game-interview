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

export interface Coord {
  x: number;
  y: number;
}

/** Immutable representation of the state of the game. */
export type GameState = {
  snake: Coord[];
  apple: Coord;
  direction: Key;
};

/** Creates an initial game state. */
export function initialState(): GameState {
  return {
    snake: [
      { x: 21, y: 20 },
      { x: 20, y: 20 },
    ],
    apple: { x: 30, y: 20 },
    direction: Key.Right,
  };
}

const computeHead = (coord: Coord, direction: Key, keyPressed: Key) => {
  let decidedDirection = direction;
  if (direction === Key.Right && keyPressed === Key.Left)
    switch (decidedDirection) {
      case Key.Left:
        return { ...coord, x: coord.x - 1 };
      case Key.Up:
        return { ...coord, y: coord.y - 1 };
      case Key.Down:
        return { ...coord, y: coord.y + 1 };
      case Key.Right:
        return { ...coord, x: coord.x + 1 };
    }
};

/** Produces the game state for the next tick. */
export function tick(
  currentState: GameState,
  lastKeyPressed: Key,
): GameState | "GameOver" {
  const newHead: Coord = computeHead(
    currentState.snake[0],
    currentState.direction,
    lastKeyPressed,
  );
  let newSnake: Coord[] = [
    newHead,
    ...currentState.snake.slice(0, currentState.snake.length - 1),
  ];

  let newApple = currentState.apple;

  if (
    newSnake[0].x === currentState.apple.x &&
    newSnake[0].y === currentState.apple.y
  ) {
    newSnake = [...newSnake, currentState.snake[currentState.snake.length - 1]];
    while (
      newSnake.findIndex((i) => i.x === newApple.x && i.y === newApple.y) !== -1
    ) {
      newApple.x = Math.floor(Math.random() * 40);
      newApple.y = Math.floor(Math.random() * 40);
    }
  }

  if (
    newHead.x >= WIDTH ||
    newHead.x < 0 ||
    newHead.y >= HEIGHT ||
    newHead.y < 0 ||
    newSnake
      .slice(1)
      .findIndex((i) => i.x === newHead.x && i.y === newHead.y) !== -1
  )
    return "GameOver";
  return {
    ...currentState,
    snake: newSnake,
    apple: newApple,
  };
}

/** Determines the color of each pixel on the screen. */
export function screenState(currentState: GameState): Array<Color> {
  return Array.from({ length: WIDTH * HEIGHT }, (_, index) => {
    const x = index % WIDTH;
    const y = Math.floor(index / HEIGHT);
    if (
      currentState.snake.findIndex((i) => {
        return i.x === x && i.y === y;
      }) !== -1
    )
      return Color.White;
    else if (currentState.apple.x === x && currentState.apple.y === y)
      return Color.Red;
    return Color.Black;
  });
}
