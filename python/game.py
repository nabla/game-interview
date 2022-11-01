from dataclasses import dataclass
from random import randint
from typing import *
from enum import Enum, auto

WIDTH = 20
HEIGHT = 20

class Key(Enum):
    """Keys that the user can press."""
    SPACE = auto()
    LEFT = auto()
    RIGHT = auto()

class Color(Enum):
    """Possible colors for pixels on screen."""
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

class GameOver(Exception):
    """Exception to raise when the game is over."""

class Matrix:
    def __init__(self, width: int, height: int, initial_value: bool):
        self.pixels = [initial_value] * width * height
        self.width = width
        self.height = height

    def __getitem__(self, key: Tuple[int, int]) -> bool:
        x, y = key
        return self.pixels[x + y * self.width]

    def __setitem__(self, key: Tuple[int, int], item: bool):
        x, y = key
        self.pixels[x + y * self.width] = item

    def rotated_clockwise(self) -> "Matrix":
        rotated = Matrix(self.width, self.height, False)
        for x in range(self.width):
            for y in range(self.height):
                rotated[self.height - 1 - y, x] = self[x, y]
        return rotated

    def copy_line(self, from_y: int, to_y: int):
        for x in range(self.width):
            self[x, to_y] = self[x, from_y]

    def clear_line(self, y: int):
        for x in range(self.width):
            self[x, y] = False

    def collapse_line_down(self, y: int):
        for y2 in reversed(range(y)):
            self.copy_line(y2, y2 + 1)
        self.clear_line(0)

    @classmethod
    def from_list(cls, pixels: List[int]) -> "Matrix":
        width = len(pixels[0])
        height = len(pixels)
        m = Matrix(width, height, False)
        for x in range(width):
            for y in range(height):
                m[x, y] = pixels[y][x]
        return m

PIECE_SHAPES = [
    Matrix.from_list([
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]),
    Matrix.from_list([
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]),
    Matrix.from_list([
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 1],
    ]),
    Matrix.from_list([
        [0, 0, 0],
        [1, 1, 1],
        [1, 0, 0],
    ]),
    Matrix.from_list([
        [0, 0, 0],
        [0, 1, 1],
        [1, 1, 0],
    ]),
    Matrix.from_list([
        [0, 0, 0],
        [1, 1, 1],
        [0, 1, 0],
    ]),
    Matrix.from_list([
        [0, 0, 0],
        [1, 1, 0],
        [0, 1, 1],
    ]),
]

class Piece(NamedTuple):
    shape: Matrix
    origin_x: int
    origin_y: int

    @classmethod
    def random(cls) -> "Piece":
        shape = PIECE_SHAPES[randint(0, len(PIECE_SHAPES) - 1)]
        origin_x = WIDTH // 2 - (shape.width // 2)
        origin_y = -shape.height
        return Piece(shape, origin_x, origin_y)

    def rotated_clockwise(self) -> "Piece":
        return self._replace(shape=self.shape.rotated_clockwise())

    def moved_left(self) -> "Piece":
        return self._replace(origin_x=self.origin_x - 1)

    def moved_right(self) -> "Piece":
        return self._replace(origin_x=self.origin_x + 1)

    def moved_down(self) -> "Piece":
        return self._replace(origin_y=self.origin_y + 1)

    def pixels(self) -> Iterator[Tuple[int, int]]:
        for piece_x in range(self.shape.width):
            for piece_y in range(self.shape.height):
                if self.shape[piece_x, piece_y]:
                    yield piece_x + self.origin_x, piece_y + self.origin_y

    def valid_for(self, background: Matrix) -> bool:
        """Whether the piece fits inside the screen and doesn't touch any pixel the background."""
        for x, y in self.pixels():
            if x < 0 or x >= WIDTH: return False
            if y < 0: continue # Negative values of y are allowed.
            if y >= HEIGHT: return False
            if background[x, y]: return False
        return True

    def try_freeze_into(self, background: Matrix):
        """Adds the piece to the background pixels, throwing if the piece can't fit inside the screen."""
        for x, y in self.pixels():
            if x < 0 or x >= WIDTH: raise GameOver()
            if y < 0 or y >= HEIGHT: raise GameOver()
            background[x, y] = True

@dataclass
class GameState:
    """State of the game."""
    step: int = 0
    current_piece: Piece = Piece.random()
    background: Matrix = Matrix(WIDTH, HEIGHT, False)

MOVE_DOWN_EVERY_TICKS = 10

def tick(current_state: GameState, key_pressed: Optional[Key]) -> GameState:
    # Move the piece left and right, ignoring invalid movements.
    moved_piece = current_state.current_piece
    if key_pressed == Key.SPACE:
        moved_piece = current_state.current_piece.rotated_clockwise()
    elif key_pressed == Key.LEFT:
        moved_piece = current_state.current_piece.moved_left()
    elif key_pressed == Key.RIGHT:
        moved_piece = current_state.current_piece.moved_right()

    if moved_piece.valid_for(current_state.background):
        current_state.current_piece = moved_piece

    # Try to move the piece down.
    if current_state.step == 0:
        moved_down_piece = current_state.current_piece.moved_down()

        if moved_down_piece.valid_for(current_state.background):
            current_state.current_piece = moved_down_piece
        else:
            # If it cannot be moved down, freeze it into the background.
            # Might raise GameOver if the piece cannot fit inside the screen.
            current_state.current_piece.try_freeze_into(current_state.background)

            # Since new pixels have been added to the background, collapse all full lines.
            for y in range(HEIGHT):
                if all(current_state.background[x, y] for x in range(WIDTH)):
                    current_state.background.collapse_line_down(y)

            # Generate a new piece, or raise GameOver if not possible.
            current_state.current_piece = Piece.random()
            if not current_state.current_piece.valid_for(current_state.background):
                raise GameOver()

    current_state.step = (current_state.step + 1) % MOVE_DOWN_EVERY_TICKS
    return current_state

def draw(game_state: GameState, set_color: Callable[[int, int, Color], Any]):
    for x, y in game_state.current_piece.pixels():
        set_color(x, y, Color.RED)

    for x in range(WIDTH):
        for y in range(HEIGHT):
            if game_state.background[x, y]:
                set_color(x, y, Color.WHITE)

if __name__ == "__main__":
    from main import run
    run()