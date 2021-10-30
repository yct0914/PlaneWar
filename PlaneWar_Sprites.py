from math import gamma
from random import randint
from random import randrange
import random
from time import sleep
from typing import overload
from pygame import *
import pygame
from pygame.sprite import *


# 屏幕大小的常量
SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
#敌机大小常量
ENEMY_RECT = pygame.Rect(0,0,57,43)
#英雄大小常量
HERO_RECT = pygame.Rect(0,0,102,126)
#子弹大小常量
BULLET_RECT = pygame.Rect(0,0,5,11)
# 刷新的帧率
FRAME_PER_SEC = 60
# 创建敌机的定时器常量
CREATE_ENEMY_EVENT = pygame.USEREVENT
# 英雄发射子弹事件
HERO_FIRE_EVENT = pygame.USEREVENT + 1

class GameSprite(Sprite):
    '''游戏精灵类'''
    def __init__(self,imageName) -> None:
        super().__init__()
        self.image = pygame.image.load(imageName)
        self.rect = self.image.get_rect()
        pass
    def update(self):   
        pass
    pass
class Background(GameSprite):
    '''游戏背景精灵类'''
    def __init__(self,is_alt = False) -> None:
        super().__init__('./images/background.png')
    def update(self): 
        pass
    pass
class Bullet(GameSprite):
    '''子弹总类'''
    def __init__(self,imageName) -> None:
        super().__init__(imageName)
        pass
    def update(self):
        pass
    pass
class EnemyBullet(Bullet):
    '''敌机子弹类'''
    def __init__(self,enemy) -> None:
        self.imageName = './images/bullet1.png'
        super().__init__(self.imageName)
        #设置子弹发射的位置
        self.rect.y = enemy.rect.y + 20
        self.rect.x = enemy.shootX + 24
        self.speed = 5
        pass
    def update(self):
        '''子弹位置的更新'''
        self.rect.y += self.speed
        if self.rect.top >= 700:
            self.kill()
            pass
        pass
    pass

class EnemyPlane(GameSprite):
    '''敌机类'''
    def __init__(self) -> None:
        self.imageName = './images/enemy1.png'
        super().__init__(self.imageName)
        self.speed = 2  #确定敌机移动速度
        self.rect.y = random.randrange(0,150,40)   #确定敌机出现的初始Y坐标值
        self.LOR = self.L_Or_R()    #确定敌机出现的初始位置，左或者右
        self.shootX = random.randrange(0,480,10)    #确定敌机发射子弹的X坐标
        self.isAlive = True #判断敌机是否存活
        self.count = 0  #用作爆炸时飞机图片更新计数
        pass
    def L_Or_R(self):
        '''敌机随机从左侧或右侧飞出'''
        temp = random.randint(0,1)
        if temp == 0:
            self.rect.x = 0
            return 'LEFT'
            pass
        else:
            self.rect.x = SCREEN_RECT.width
            return 'RIGHT'
            pass
        pass
    def moveLeft(self):
        if self.rect.x > -57:
            self.rect.x -= self.speed
            pass
        elif self.rect.x <= -57:
            self.kill()
        pass
    def moveRight(self):
        if self.rect.x < 480:
            self.rect.x += self.speed
            pass
        elif self.rect.x >= 480:
            self.kill()
        pass
    def update(self):
        if self.LOR == 'LEFT':
            self.moveRight()
            pass
        elif self.LOR == 'RIGHT':
            self.moveLeft()
            pass
        if self.isAlive == False:
            '''当飞机被击中时连着四次更新飞机的image路径以达到爆炸效果图片'''
            self.X = self.rect.x
            self.Y = self.rect.y
            if self.count == 0:
                self.image = pygame.image.load('./images/enemy1_down1.png')
                self.rect = self.image.get_rect()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            elif self.count == 1:
                self.image = pygame.image.load('./images/enemy1_down1.png')
                self.rect.size = self.image.get_size()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            elif self.count == 2:
                self.image = pygame.image.load('./images/enemy1_down1.png')
                self.rect.size = self.image.get_size()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            elif self.count == 3:
                self.image = pygame.image.load('./images/enemy1_down1.png')
                self.rect.size = self.image.get_size()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            else:
                #在爆炸后"自杀"
                self.kill()
        pass
    pass
class HeroBullet(Bullet):
    '''英雄子弹类'''
    def __init__(self,hero) -> None:
        self.imageName = './images/bullet2.png'
        super().__init__(self.imageName)
        self.rect.x = hero.rect.x + 48.5
        self.rect.y = hero.rect.y - 11
        self.speed = 5
        pass
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
            pass
        pass
   
    pass
class Hero(GameSprite):
    '''英雄飞机类'''
    def __init__(self) -> None:
        self.imageName = './images/me1.png'
        super().__init__(self.imageName)
        self.rect.x = 189
        self.rect.y = 574
        self.speed = 5
        self.bullets = pygame.sprite.Group()    #英雄发射的子弹精灵组初始化
        self.isAlive = True
        self.count = 0
        pass
    def moveLeft(self):
        if self.rect.x > 0:
            self.rect.x -= self.speed
            pass
        pass
    def moveRight(self):
        if self.rect.x < SCREEN_RECT.width - HERO_RECT.width:
            self.rect.x += self.speed
            pass
        pass
    def shoot(self):
        '''发射子弹函数'''
        bullet = HeroBullet(self)
        self.bullets.add(bullet)
        pass
    def update(self):
        if self.isAlive == False:
            '''飞机被子弹击中时更新的图片,同上'''
            self.X = self.rect.x
            self.Y = self.rect.y
            if self.count == 0:
                self.image = pygame.image.load('./images/me_destroy_1.png')
                self.rect = self.image.get_rect()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            elif self.count == 1:
                self.image = pygame.image.load('./images/me_destroy_2.png')
                self.rect.size = self.image.get_size()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            elif self.count == 2:
                self.image = pygame.image.load('./images/me_destroy_3.png')
                self.rect.size = self.image.get_size()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            elif self.count == 3:
                self.image = pygame.image.load('./images/me_destroy_4.png')
                self.rect.size = self.image.get_size()
                self.rect.x = self.X
                self.rect.y = self.Y
                self.count += 1
                pass
            else:
                self.kill()
                #英雄爆炸后游戏结束
                gameOver()
                pass
            pass
        pass
    pass
# class Button(GameSprite):
#     '''按钮精灵'''
#     def __init__(self, imageName,type) -> None:
#         super().__init__(imageName)
#         self.type = type
#         pass
#     def setXY(self):
#         if type == 'AGAIN':
#             self.rect.x = 240-150
#             self.rect.y = 300
#             pass
#         elif type == 'OVER':
#             self.rect.x = 240-150
#             self.rect.y = 300+59
#             pass
#         elif type == 'PAUSE':
#             self.rect.x = 0
#             self.rect.y = 655
#             pass
#         elif type == 'BEGIN':
#             self.rect.x = 0
#             self.rect.y = 655
#             pass
#         pass
#     def update(self):
#         pass       
#     pass
def gameOver():
        pygame.quit()
        exit()
        pass
    
a = pygame.image.load('./images/pause_nor.png')
print(a.get_height(),a.get_width())
