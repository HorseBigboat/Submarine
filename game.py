import pygame
import random
from pygame.locals import *
from sys import exit
from random import randint


class Hero(pygame.sprite.Sprite):  # 英雄类
    def __init__(self, hero_image, hero_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hero_image
        self.rect = self.image.get_rect()
        self.rect.topleft = hero_init_pos
        self.speed = 6
        self.bombgroup = pygame.sprite.Group()

    def move(self, offset):  # 定义英雄移动
        x = self.rect.left + offset[pygame.K_RIGHT] - offset[pygame.K_LEFT]
        if x < 0:
            self.rect.left = 0
        elif x > SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left = x

    def single_bomb(self, bomb_image):  # 定义单个炸弹，与英雄绑定
        single_bomb = Bomb(bomb_image, self.rect.midtop)
        self.bombgroup.add(single_bomb)


class Bomb(pygame.sprite.Sprite):  # 炸弹类
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


class Enemy(pygame.sprite.Sprite):  # 敌人类
    def __init__(self, enemy_image, enemy_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.topleft = enemy_init_pos
        self.speed = 2
        self.minepos = random.randrange(0, 640, 2)

    def update(self):
        self.rect.left += self.speed
        if self.rect.left > SCREEN_WIDTH:
            self.kill()


class Mine(pygame.sprite.Sprite):  # 敌人水雷类
    def __init__(self, mine_image, mine_init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = mine_image
        self.rect = self.image.get_rect()
        self.rect.topleft = mine_init_pos
        self.speed = 2
        self.clock = 0

    def update(self):
        if self.rect.top <= 90:
            self.rect.top = 90
            self.clock += 1
            if self.clock == 100:
                self.kill()
        else:
            self.rect.top -= self.speed


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FRAME_RATE = 60
ANIMATE_CYCLE = 60

ticks = 0
clock = pygame.time.Clock()
offset = {pygame.K_LEFT: 0, pygame.K_RIGHT: 0}

background = pygame.image.load('sea.png')
hero_img = pygame.image.load('hero.png')
hero_pos = [300, 80]
bomb_img = pygame.image.load('bomb.png')
enemy_img = pygame.image.load('enemy.png')
gameover = pygame.image.load('gameover.png')

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("MINE")

hero = Hero(hero_img, hero_pos)

enemy_group = pygame.sprite.Group()
enemy_down_group = pygame.sprite.Group()

mine_group = pygame.sprite.Group()

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
    enemy_group.draw(screen)
    enemy_group.update()

    for enemy in enemy_group:
        if enemy.rect.left == enemy.minepos:
            mine_pos = [enemy.rect.left, enemy.rect.top]
            mine = Mine(mine_image=pygame.image.load(
                "mine.png"), mine_init_pos=mine_pos)
            mine_group.add(mine)
    mine_group.draw(screen)
    mine_group.update()

    # 此处加入minegroup和hero的碰撞,碰撞后跳出循环，显示gameover界面
    boom = None
    boom = pygame.sprite.spritecollideany(hero, mine_group)
    if boom is not None:
        mine_group.remove(mine)
        break

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

        elif event.type == pygame.KEYUP:
            if event.key in offset:
                offset[event.key] = 0

    hero.bombgroup.update()
    hero.bombgroup.draw(screen)
    hero.move(offset)

    pygame.display.update()

screen.blit(gameover, (0, 0))
while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
