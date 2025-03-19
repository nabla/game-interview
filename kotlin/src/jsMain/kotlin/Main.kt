import kotlinx.browser.document
import kotlinx.browser.window
import org.w3c.dom.HTMLElement
import org.w3c.dom.HTMLDivElement
import org.w3c.dom.events.KeyboardEvent

fun main() {
    val gameZone = document.getElementById("game-zone") as HTMLElement
    gameZone.focus()

    var lastKeyPressed = Key.ArrowRight
    gameZone.addEventListener("keydown", { event ->
        val ke = event as KeyboardEvent
        lastKeyPressed = when (ke.key) {
            "ArrowUp" -> Key.ArrowUp
            "ArrowDown" -> Key.ArrowDown
            "ArrowLeft" -> Key.ArrowLeft
            "ArrowRight" -> Key.ArrowRight
            else -> lastKeyPressed
        }
    })

    val gameContainer = document.getElementById("game") as HTMLElement
    val pixels = ArrayList<HTMLDivElement>(WIDTH * HEIGHT)
    repeat(HEIGHT) {
        repeat(WIDTH) {
            val cell = document.createElement("div") as HTMLDivElement
            gameContainer.appendChild(cell)
            pixels.add(cell)
        }
    }

    val game = MyGame()

    fun loop() {
        try {
            game.tick(lastKeyPressed)
        } catch (e: Error) {
            pixels.forEach {
                it.style.backgroundColor = Color.Red.hex
            }
            return
        }

        pixels.forEach {
            it.style.backgroundColor = "#000000"
        }

        game.draw { x, y, color ->
            if (x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT) return@draw
            val pixel = pixels[y * WIDTH + x]
            pixel.style.backgroundColor = color.hex
        }

        window.setTimeout(::loop, 50)
    }

    loop()
}
