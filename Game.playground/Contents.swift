import PlaygroundSupport

class SnakeGame: Game {
    let width: Int = 30
    let height: Int = 20

    /// Any state that needs to be persisted between ticks of the game.
    struct State {}
    var initialState: State { State() }

    /// Transforms the current state into the next given some keyboard input, throwing when losing.
    /// Possible values of lastInput: `.keyUp, .keyDown, .keyLeft, .keyRight` .
    func tick(state: State, lastInput: Input) throws -> State {
        state
    }

    /// Draws the given state into a buffer of pixels.
    ///
    /// Examples:
    /// ```
    /// buffer[x, y] = .white
    /// buffer[x, y] = .red
    /// ```
    func draw(state: State, buffer: inout Buffer) {}
}

struct GameOverError: Error {}

let game = SnakeGame()
let gameView = GameView(game: game)
gameView.start()
