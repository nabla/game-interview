import pygame
from pygame.locals import *
from game import WIDTH, HEIGHT, Key, GameState, tick, draw

FPS = 10
ZOOM = 15

def run():
    pygame.init()
    pygame.display.set_caption("Nabla Playground")

    screen = pygame.display.set_mode((WIDTH * ZOOM, HEIGHT * ZOOM))
    clock = pygame.time.Clock()
    
    running = True
    game_state = GameState()
    last_key_pressed = Key.RIGHT
    
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                else:
                    match event.key:
                        case pygame.K_LEFT:
                            last_key_pressed = Key.LEFT
                        case pygame.K_RIGHT:
                            last_key_pressed = Key.RIGHT
                        case pygame.K_UP:
                            last_key_pressed = Key.UP
                        case pygame.K_DOWN:
                            last_key_pressed = Key.DOWN
            elif event.type == QUIT:
                running = False
        
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((0, 0, 0))

        game_state = tick(game_state, last_key_pressed)
        draw(game_state, lambda x, y, color: surface.set_at((x, y), color.value))

        pygame.transform.scale(surface, (WIDTH * ZOOM, HEIGHT * ZOOM), screen)
        pygame.display.flip()

if __name__ == "__main__":
    run()