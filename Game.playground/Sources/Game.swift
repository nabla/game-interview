import AppKit
import PlaygroundSupport

// MARK: -- Game protocol.

public protocol Game {
    associatedtype State

    var width: Int { get }
    var height: Int { get }
    var initialState: State { get }

    func tick(state: State, lastInput: Input) throws -> State
    func draw(state: State, buffer: inout Buffer)
}

// MARK: -- Utilities.

public enum Input {
    case keyUp
    case keyDown
    case keyLeft
    case keyRight

    init?(keyCode: UInt16) {
        switch keyCode {
        case 126:
            self = .keyUp
        case 125:
            self = .keyDown
        case 123:
            self = .keyLeft
        case 124:
            self = .keyRight
        default:
            return nil
        }
    }
}

public enum Color {
    case black
    case white
    case red

    var cgColor: CGColor {
        switch self {
        case .black:
            return .black
        case .white:
            return .white
        case .red:
            return CGColor(red: 1, green: 0, blue: 0, alpha: 1)
        }
    }
}

public struct Buffer {
    let width: Int
    let height: Int
    private var storage: [CGColor?]

    init(width: Int, height: Int) {
        self.width = width
        self.height = height
        storage = .init(repeating: nil, count: width * height)
    }

    public subscript(x: Int, y: Int) -> CGColor? {
        get {
            storage[(x * height) + y]
        }
        set {
            storage[(x * height) + y] = newValue
        }
    }

    mutating func clear() {
        storage = .init(repeating: nil, count: width * height)
    }
}

// MARK: -- Game engine.

public class GameView<G: Game>: NSView {
    public override var acceptsFirstResponder: Bool { true }

    let game: G
    let interval: Double

    var timer: Timer?
    var currentBuffer: Buffer
    var currentState: G.State
    var lastInput: Input = .keyRight

    public init(game: G, scale: Int = 20, interval: Double = 0.1) {
        self.game = game
        self.interval = interval

        self.currentBuffer = Buffer(width: game.width, height: game.height)
        self.currentState = game.initialState

        let size = CGSize(width: game.width * scale, height: game.height * scale)
        super.init(frame: CGRect(origin: .zero, size: size))
        scaleUnitSquare(to: CGSize(width: scale, height: scale))
    }

    public func start() {
        let timer = Timer(timeInterval: interval, target: self, selector: #selector(update), userInfo: nil, repeats: true)
        RunLoop.current.add(timer, forMode: .common)
        self.timer = timer
        PlaygroundPage.current.liveView = self
    }

    required init?(coder: NSCoder) {
        fatalError("Not implemented.")
    }

    // Runs every [interval] seconds, blocks the main thread.
    @objc func update() {
        do {
            try self.currentState = game.tick(state: self.currentState, lastInput: lastInput)
        } catch {
            showGameOver()
        }

        self.currentBuffer.clear()
        game.draw(state: self.currentState, buffer: &self.currentBuffer)

        needsDisplay = true
    }

    private func showGameOver() {
        let size = CGSize(width: 30 * 20, height: 20 * 20)
        let frame = CGRect(origin: .zero, size: size)
        let textField = NSTextField(frame: frame)
        textField.isEditable = false
        textField.stringValue = #"""







           ____                                            _
          / ___| __ _ _ __ ___   ___    _____   _____ _ __| |
         | |  _ / _` | '_ ` _ \ / _ \  / _ \ \ / / _ \ '__| |
         | |_| | (_| | | | | | |  __/ | (_) \ V /  __/ |  |_|
          \____|\__,_|_| |_| |_|\___|  \___/ \_/ \___|_|  (_)
        """#

        textField.alignment = .center
        textField.font = NSFont(name: "Menlo", size: 16)
        textField.textColor = .red
        textField.backgroundColor = .black
        self.timer?.invalidate()
        PlaygroundPage.current.liveView = textField
    }

    override open func draw(_ rect: CGRect) {
        let context = NSGraphicsContext.current!.cgContext

        // Draw the background as a whole for performance reasons.
        context.setFillColor(.black)
        context.fill(CGRect(origin: .zero, size: CGSize(width: game.width, height: game.height)))

        // Draw only the non-nil pixels of the buffer afterwards.
        for i in 0..<game.width {
            for j in 0..<game.height {
                if let color = currentBuffer[i, j] {
                    context.setFillColor(color)
                    context.fill(
                        CGRect(origin: CGPoint(x: i, y: game.height - j - 1),
                               size: CGSize(width: 1, height: 1))
                    )
                }
            }
        }
    }

    // Responds to keyboard events, blocks the main thread.
    override open func keyDown(with event: NSEvent) {
        if let input = Input(keyCode: event.keyCode) {
            lastInput = input
        }
    }
}
