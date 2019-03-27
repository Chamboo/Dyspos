import pygame
import time
import math

from objects import *
pygame.init()


def main():
    global event
    run = True
    setup()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        events()

        logic()
        draw()
        count_fps()


def setup():
    global window, height, width, player, camera, projectiles, clicked, cSec, cFrame, FPS, deltatime, previous, fpsFont
    global cooldown, pressed, enemies, hudFont
    clicked = False
    projectiles = []
    enemies = [Enemy(10, 10, 100)]
    height = 1080
    width = 1920
    window = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    pygame.display.set_caption("Dyspos")
    cSec = 0
    cFrame = 0
    pressed = False
    FPS = 0
    deltatime = 0
    cooldown = 0
    previous = time.time()
    player = Player()
    camera = Camera()
    fpsFont = pygame.font.Font("fonts\\Verdana.ttf", 18)
    hudFont = pygame.font.Font("fonts\\Verdana.ttf", 30)

def draw():
    global projectiles, enemies

    # background

    window.fill((125, 125, 255))

    # Terrain

    for x in range(30):
        for y in range(15):
            if y % 2 == 0 and x % 2 == 0:
                pass
            elif x % 2 == 0 or y % 2 == 0:
                pygame.draw.rect(window, (0, 222, 0), ((x + camera.x) * 64, (y + camera.y) * 64, 64, 64))

    # Entities

    pygame.draw.rect(window, (0, 125, 125), (player.screenX, player.screenY, player.width, player.height))

    for i in range(len(projectiles)):
        pygame.draw.rect(window, (255, 0, 0), ((projectiles[i].x-16) + camera.x*64, (projectiles[i].y - 16)+ camera.y * 64, projectiles[i].width, projectiles[i].height))


    for enemy in enemies:
        pygame.draw.rect(window, (255, 125, 125), ((enemy.x - 32) + camera.x * 64, (enemy.y - 32) + camera.y * 64, enemy.width, enemy.height))
        pygame.draw.rect(window, (100, 100, 100), ((enemy.x - 41) + camera.x * 64, (enemy.y - 61) + camera.y * 64, 82, 12))
        pygame.draw.rect(window, (160, 160, 160), ((enemy.x - 40) + camera.x * 64, (enemy.y - 60) + camera.y * 64, 80, 10))
        pygame.draw.rect(window, (255, 0, 0), ((enemy.x - 40) + camera.x * 64, (enemy.y - 60) + camera.y * 64, math.floor(80 * (player.health/player.maxHealth)), 10))


    # Hud
    # Health Bar
    pygame.draw.rect(window, (100, 100, 100), (198, 998, 704, 64))
    pygame.draw.rect(window, (160, 160, 160), (200, 1000, 700, 60))
    pygame.draw.rect(window, (255, 0, 0), (200, 1000, math.floor(700 * (player.health/player.maxHealth)), 60))
    window.blit(hudFont.render(("HEALTH: " + str(math.floor(player.health))), True, (0, 0, 0)), (210, 1010))

    # Mana Bar
    pygame.draw.rect(window, (100, 100, 100), (1018, 998, 704, 64))
    pygame.draw.rect(window, (160, 160, 160), (1020, 1000, 700, 60))
    pygame.draw.rect(window, (0, 0, 255), (1020, 1000, math.floor(700 * (player.mana/player.maxMana)), 60))
    window.blit(hudFont.render(("MANA: " + str(player.mana)), True, (0, 0, 0)), (1030, 1010))

    show_fps()
    pygame.display.update()


def events():
    global player, camera, projectiles, clicked, cooldown, pressed
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        camera.x += 10 * deltatime

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera.x -= 10 * deltatime

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        camera.y += 10 * deltatime

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera.y -= 10 * deltatime

    if keys[pygame.K_ESCAPE]:
        pygame.quit()


    if pygame.mouse.get_pressed()[0] == 1:
        pressed = True

    if pressed:
        if not clicked:
            mousepos = pygame.mouse.get_pos()
            projectiles.append(Projectile(camera.x, camera.y, mousepos[0] - camera.x*64, mousepos[1]-camera.y*64))
            clicked = True
            cooldown = 0

    if clicked:
        cooldown += deltatime
        if cooldown >= 1:
            clicked = False

    if pygame.mouse.get_pressed()[0] == 0:
        pressed = False


def logic():
    global projectiles
    for projectile in projectiles:
        projectile.x += projectile.xSpeed * deltatime
        projectile.y += projectile.ySpeed * deltatime
        projectile.time += deltatime

    for i in range(len(projectiles)):
        if projectiles[i].time > 0.5:
            del projectiles[i]
            break


    for enemy in enemies:
        enemy.changeDirection(camera.x, camera.y)
        enemy.x += enemy.xSpeed * deltatime
        enemy.y += enemy.ySpeed * deltatime

def count_fps():
    global cSec, cFrame, FPS, deltatime, previous

    if cSec == time.strftime("%S"):
        cFrame += 1
    else:
        FPS = cFrame
        cFrame = 0
        cSec = time.strftime("%S")

    deltatime = time.time() - previous
    previous = time.time()


def show_fps():
    fps_overlay = fpsFont.render(("FPS:" + str(FPS)), True, (0, 0, 0))
    window.blit(fps_overlay, (5, 5))


if __name__ == '__main__':
    main()

pygame.quit()
