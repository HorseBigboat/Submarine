import pygame
from pygame.locals import *
from sys import exit
from random import randint


class Hero(pygame.sprite.Sprite):
    def __init__(self, hero_image, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_image
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        self.bombgroup = pygame.sprite.Group()

    def move(self, offset):
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

    def single_bomb(self, bomb_image):
        single_bomb = Bomb(bomb_image, self.rect.midtop)
        self.bombgroup.add(single_bomb)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, bomb_image, bomb_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bomb_image
        self.rect = self.image.get_rect()
        self.rect.topleft = bomb_init_pos
        self.speed = 3

    def update(self):
        self.rect.top += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Mine(pygame.sprite.Sprite):
    def __init__(self, mine_image, mine_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = mine_image
        self.rect = self.image.get_rect()
        self.rect.topleft = mine_init_pos
        self.speed = 3

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top == 100:
            self.kill()



class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_image, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 2
        self.minegroup = pygame.sprite.Group()

    def update(self):
        self.rect.left += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

    def single_mine(self, mine_image):
        single_mine = Mine(mine_image, self.rect.midtop)
        self.minegroup.add(single_mine)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FRAME_RATE = 60
ANIMATE_CYCLE = 60

ticks = 0
clock = pygame.time.Clock()
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0}

hero_pos = [300, 80]

background = pygame.image.load('sea.png')
hero_img = pygame.image.load('hero.png')
bomb_img = pygame.image.load('bomb.png')
enemy_img = pygame.image.load('enemy.png')
mine_img = pygame.image.load('mine.png')

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("MINE")

hero = Hero(hero_img, hero_pos)

enemy_group = pygame.sprite.Group()
enemy_down_group = pygame.sprite.Group()

enemy_pos = [-enemy_img.get_width(), randint(120, 460)]
enemy = Enemy(enemy_img, enemy_pos)
enemy_group.add(enemy)

while True:
    clock.tick(FRAME_RATE)
    if ticks >= ANIMATE_CYCLE:
        ticks = 0

    screen.blit(background, (0, 0))
    screen.blit(hero.image, hero.rect)
    ticks += 1

    if ticks % 60 == 0:
        enemy_pos = [-enemy_img.get_width(), randint(120, 460)]
        enemy = Enemy(enemy_img, enemy_pos)
        enemy_group.add(enemy)

    enemy_group.update()
    enemy_group.draw(screen)

    enemy_down_group.add(
        pygame.sprite.groupcollide(
            enemy_group,
            hero.bombgroup,
            True,
            True))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key in offset:
                offset[event.key] = hero.speed
            if event.key == K_SPACE:
                hero.single_bomb(bomb_img)
                enemy.single_mine(mine_img)

        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0

    hero.bombgroup.update()
    hero.bombgroup.draw(screen)
    hero.move(offset)

    enemy.minegroup.update()
    enemy.minegroup.draw(screen)

    pygame.display.update()
