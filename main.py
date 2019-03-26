import pygame
import time

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
    global cooldown, pressed, enemies
    clicked = False
    projectiles = []
    enemies = [Enemy(10, 10)]
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


def draw():
    global projectiles, enemies
    window.fill((125, 125, 255))

    for x in range(-30, 30):
        for y in range(-30, 30):
            if y % 2 == 0 and x % 2 == 0:
                pass
            elif x % 2 == 0 or y % 2 == 0:
                pygame.draw.rect(window, (0, 255, 0), ((x + camera.x) * 64, (y + camera.y) * 64, 64, 64))

    pygame.draw.rect(window, (0, 125, 125), (player.screenX, player.screenY, player.width, player.height))

    for enemy in enemies:
        pygame.draw.rect(window, (255, 125, 125), ((enemy.x - 16) + camera.x*64, (enemy.y - 16) + camera.y * 64, enemy.width, enemy.height))

    for i in range(len(projectiles)):
        pygame.draw.rect(window, (255, 0, 0), ((projectiles[i].x-16) + camera.x*64, (projectiles[i].y - 16)+ camera.y * 64, projectiles[i].width, projectiles[i].height))

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

    if event.type == pygame.MOUSEBUTTONDOWN:
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

    if event.type == pygame.MOUSEBUTTONUP:
        pressed = False


def logic():
    global projectiles
    for projectile in projectiles:
        projectile.x += projectile.xSpeed * deltatime
        projectile.y += projectile.ySpeed * deltatime

    for i in range(len(projectiles)):
        if 2100 < (projectiles[i].x-16) + camera.x*64 or (projectiles[i].x-16) + camera.x*64 < -100 or \
                1280 < (projectiles[i].y - 16) + camera.y*64 or (projectiles[i].y - 16) + camera.y*64 < -100:
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
