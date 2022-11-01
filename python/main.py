import pygame
from typing import *
from pygame.locals import *
from game import WIDTH, HEIGHT, Key, GameState, tick, draw

FPS = 60
ZOOM = 15

def run():
    pygame.init()
    pygame.display.set_caption("Nabla Playground")

    screen = pygame.display.set_mode((WIDTH * ZOOM, HEIGHT * ZOOM))
    clock = pygame.time.Clock()
    
    running = True
    fps_boost = False
    game_state = GameState()

    while running:
        clock.tick(FPS * (5 if fps_boost else 1))
        key_pressed: Optional[Key] = None

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_LEFT:
                    key_pressed = Key.LEFT
                elif event.key == K_RIGHT:
                    key_pressed = Key.RIGHT
                elif event.key == K_SPACE:
                    key_pressed = Key.SPACE
                elif event.key == K_DOWN:
                    fps_boost = True
            elif event.type == KEYUP and event.key == K_DOWN:
                fps_boost = False
            elif event.type == QUIT:
                running = False
        
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill((0, 0, 0))

        game_state = tick(game_state, key_pressed)
        draw(game_state, lambda x, y, color: surface.set_at((x, y), color.value))

        pygame.transform.scale(surface, (WIDTH * ZOOM, HEIGHT * ZOOM), screen)
        pygame.display.flip()

if __name__ == "__main__":
    run()