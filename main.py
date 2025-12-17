import sys

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import MAX_LIVES, SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_event, log_state
from player import Player
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    AsteroidField()

    p = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    a_killed = 0
    dt_passed = 0

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(p):
                if p.shots_fired == 0:
                    accuracy = 0
                else:
                    accuracy = a_killed / p.shots_fired
                score = (round(dt_passed / 100) + (a_killed * 3)) * (accuracy * 2)
                log_event("player_hit")
                print("Game over!")
                print(f"Your Score: {score}")
                print(f"Time Alive: {dt_passed / 100}")
                print(
                    f"Accuracy: {accuracy}   (Asteroids Hit: {a_killed},  Shots Fired: {p.shots_fired})"
                )

                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if shot.collides_with(asteroid):
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.kill()
                    a_killed += 1
        screen.fill("purple")
        for item in drawable:
            item.draw(screen)
        pygame.display.flip()
        tick = clock.tick(60)
        dt = tick / 1000
        dt_passed += 1


if __name__ == "__main__":
    main()
