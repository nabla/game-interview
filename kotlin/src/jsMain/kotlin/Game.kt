const val HEIGHT = 40
const val WIDTH = 40

enum class Key {
    ArrowUp,
    ArrowDown,
    ArrowLeft,
    ArrowRight,
}

enum class Direction {
    Up,
    Down,
    Left,
    Right,
}

enum class Color(val hex: String) {
    Red("#FF0000"),
    Green("#00FF00"),
    Blue("#0000FF"),
    White("#FFFFFF"),
}

interface Game {
    /**
     * Called at a regular time interval (every 50ms) to update the game state.
     * Takes the last key pressed as an argument, or `ArrowRight` if no key was pressed yet.
     * Should throw if the game reaches a "game over" condition.
     */
    fun tick(lastKeyPressed: Key): Unit

    /**
     * Called whenever the playground wants to display the internal state of the game.
     * Should call the callback function for each cell of the playground, with the color to display.
     * You can assume the playground cells all have the color black initially.
     */
    fun draw(callback: (x: Int, y: Int, color: Color) -> Unit): Unit
}

/**
 * A simple game where the player can move a pixel.
 */
class MyGame: Game {
    private var x = WIDTH / 2
    private var y = HEIGHT / 2

    override fun tick(lastKeyPressed: Key) {
        when (lastKeyPressed) {
            Key.ArrowUp -> y--
            Key.ArrowDown -> y++
            Key.ArrowLeft -> x--
            Key.ArrowRight -> x++
        }

        if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) {
            throw Error("Out of bounds")
        }
    }

    override fun draw(callback: (x: Int, y: Int, color: Color) -> Unit) {
        callback(x, y, Color.White)
    }
}