import pygame
import time

from objects import *
pygame.init()


def main():
    global event, current
    run = True
    setup()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if current == 'game':
            events()
            logic()
            draw()
            count_fps()

        if current == 'startmenu':
            print('No menu play game XD')
            current = 'game'


def setup():
    global window, height, width, player, camera, projectiles, clicked, cSec, cFrame, FPS, deltatime, previous, fpsFont
    global cooldown, enemies, hudFont, score, current
    clicked = False
    projectiles = []
    enemies = [Enemy(random.randint(1, 29), random.randint(1, 17), 100)]
    height = 1080
    width = 1920
    window = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
    pygame.display.set_caption("Dyspos")
    cSec = 0
    cFrame = 0
    FPS = 0
    deltatime = 0
    cooldown = {'projectile': 0, 'manaregen': 0, 'damage': 0, 'newE': 0}
    previous = time.time()
    player = Player()
    camera = Camera()
    fpsFont = pygame.font.Font("fonts\\Verdana.ttf", 18)
    hudFont = pygame.font.Font("fonts\\Verdana.ttf", 30)
    score = 0
    current = 'startmenu'

def draw():
    global projectiles, enemies

    # background

    window.fill((125, 125, 255))

    # Terrain

    for x in range(30):
        for y in range(18):
            if y % 2 == 0 and x % 2 == 0:
                pass
            elif x % 2 == 0 or y % 2 == 0:
                pygame.draw.rect(window, (0, 222, 0), ((x + camera.x) * 64, (y + camera.y) * 64, 64, 64))

    # Entities

    pygame.draw.rect(window, (0, 125, 125), (player.screenX, player.screenY, player.width, player.height))

    for i in range(len(projectiles)):
        pygame.draw.rect(window, (255, 0, 0), ((projectiles[i].x-16) + camera.x*64, (projectiles[i].y - 16)+ camera.y * 64, projectiles[i].width, projectiles[i].height))


    for enemy in enemies:
        pygame.draw.rect(window, enemy.colour, ((enemy.x - 32) + camera.x * 64, (enemy.y - 32) + camera.y * 64, enemy.width, enemy.height))
        pygame.draw.rect(window, (100, 100, 100), ((enemy.x - 41) + camera.x * 64, (enemy.y - 61) + camera.y * 64, 82, 12))
        pygame.draw.rect(window, (160, 160, 160), ((enemy.x - 40) + camera.x * 64, (enemy.y - 60) + camera.y * 64, 80, 10))
        pygame.draw.rect(window, (255, 0, 0), ((enemy.x - 40) + camera.x * 64, (enemy.y - 60) + camera.y * 64, math.floor(80 * (enemy.health/enemy.maxHealth)), 10))

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
    window.blit(hudFont.render(("MANA: " + str(math.floor(player.mana))), True, (0, 0, 0)), (1030, 1010))
    # Score
    window.blit(hudFont.render(("Score: " + str(score)), True, (0, 0, 0)), (10, 1010))

    show_fps()
    pygame.display.update()


def events():
    global player, camera, projectiles, clicked, cooldown
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        camera.x += 8 * deltatime

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        camera.x -= 8 * deltatime

    if keys[pygame.K_w] or keys[pygame.K_UP]:
        camera.y += 8 * deltatime

    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        camera.y -= 8 * deltatime

    if keys[pygame.K_ESCAPE]:
        pygame.quit()

    if pygame.mouse.get_pressed()[0] == 1:
        if not clicked and player.mana >= 10:
            mousepos = pygame.mouse.get_pos()
            projectiles.append(Projectile(camera.x, camera.y, mousepos[0] - camera.x*64, mousepos[1]-camera.y*64))
            clicked = True
            cooldown['projectile'] = 0
            player.mana -= 10

    if clicked:
        cooldown['projectile'] += deltatime
        if cooldown['projectile'] >= 0.3:
            clicked = False


def logic():
    global projectiles, player, score
    player.x = -camera.x*64 + 960
    player.y = -camera.y*64 + 540
    for projectile in projectiles:
        projectile.x += projectile.xSpeed * deltatime
        projectile.y += projectile.ySpeed * deltatime
        projectile.time += deltatime

    for i in range(len(projectiles)):
        if projectiles[i].time > 0.5:
            del projectiles[i]
            break

    if cooldown['manaregen'] >= 0.1 and player.mana + (1/7) <= 100:
        player.mana += 2/7
        cooldown['manaregen'] = 0

    for enemy in enemies:
        enemy.changeDirection(camera.x, camera.y)
        enemy.x += enemy.xSpeed * deltatime
        enemy.y += enemy.ySpeed * deltatime

        if checkCollision(player, enemy):
            if player.health - 5 < 0:
                player.health = 0

            elif cooldown['damage'] >= 1:
                player.health -= 5
                cooldown['damage'] = 0

        enemy.Dcooldown += deltatime

    for i in range(len(enemies)):
        for j in range(len(projectiles)):
            if checkCollision(enemies[i], projectiles[j]):
                del projectiles[j]
                if enemies[i].health - 10 <= 0:
                    enemies[i].health = 0
                    del enemies[i]
                    player.mana = player.maxMana
                    cooldown['newE'] = 0
                    score += 1

                elif enemies[i].Dcooldown >= 0.1:
                    enemies[i].health -= 10
                    enemies[i].Dcooldown = 0
                break

    if len(enemies) == 0 and cooldown['newE'] >= 1:
        enemies.append(Enemy(random.randint(1, 29), random.randint(1, 17), 100))


    cooldown['manaregen'] += deltatime
    cooldown['damage'] += deltatime
    cooldown['newE'] += deltatime


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

def checkCollision(a, b):
    return (abs(a.x - b.x) * 2 < (a.width + b.width)) and (abs(a.y - b.y) * 2 < (a.height + b.height))

if __name__ == '__main__':
    main()

pygame.quit()
