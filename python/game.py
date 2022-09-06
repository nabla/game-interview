from enum import Enum, auto
from typing import Any, Callable

WIDTH = 40
HEIGHT = 40

class Key(Enum):
    """Keys that the user can press."""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class Color(Enum):
    """Possible colors for pixels on screen."""
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

class GameOver(Exception):
    """Exception to raise when the game is over."""

class GameState:
    """Representation of the state of the game."""
    def __init__(self):
        """Creates an initial game state."""
        pass

def tick(current_game_state: GameState, last_key_pressed: Key) -> GameState:
    """
    Produces the game state for the next tick.
    Should raise `GameOver()` when the game is over.
    """
    return current_game_state

def draw(game_state: GameState, set_color: Callable[[int, int, Color], Any]):
    """
    Sets the color of each pixel on the screen to match the current game state.
    Example: set_color(x, y, Color.RED)
    """
    pass

if __name__ == "__main__":
    from main import run
    run()