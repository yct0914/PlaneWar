from math import trunc
from time import sleep
from PlaneWar_Sprites import *
import pygame

pygame.init()   #pygame模块初始化

class PlaneGame:
    '''飞机大战主游戏类'''
    def __init__(self) -> None:
        print('游戏初始化')
        self.screen = pygame.display.set_mode(SCREEN_RECT.size) #创建屏幕
        self.clock = pygame.time.Clock()    #创建时钟对象
        self.createSprites()    #调用创建精灵函数
        # 设置定时器 发射子弹和创建敌机
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,100)
        pygame.mixer.init() #初始化
        pygame.mixer.music.load('./images/background.mp3')  #加载音乐路径
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1) #循环次数
        pass
    def createSprites(self):
        '''创建精灵/组函数'''
        background1 = Background()
        background2 = Background(True)
        self.back_group = pygame.sprite.Group(background1,background2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)
        self.enemyBullets_group = pygame.sprite.Group()
        pass
    def startGame(self):
        print('游戏开始')
        '''游戏的主要循环'''
        while True:
            self.clock.tick(60)
            self.eventHandle()
            self.checkCollide()
            self.enemyShoot()
            self.update_sprites()
            pygame.display.update()
            pass
        pass
    def eventHandle(self):
        '''事件监听函数'''
        for item in pygame.event.get():
            #退出时进行的操作
            if item.type == QUIT:   
                print("退出")
                exit()
                pass
            #创建敌机
            elif item.type == CREATE_ENEMY_EVENT:
                enemy = EnemyPlane()
                self.enemy_group.add(enemy)
                pass
            #英雄自动发射子弹
            elif item.type == HERO_FIRE_EVENT:
                self.hero.shoot()
                pass
            pass
        #控制英雄左右移动
        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed = pygame.key.get_pressed()
        # 判断元组中对应的按键索引值 1
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            self.hero.moveRight()
            pass
        elif keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            self.hero.moveLeft()
            pass

        pass  
    def enemyShoot(self):
        '''敌机发射子弹'''
        for enemy in self.enemy_group:
            if enemy.shootX == enemy.rect.x:    #当敌机运动到随机的x坐标时发射子弹
                self.enemyBullets_group.add(EnemyBullet(enemy))#创建敌机子弹并加入精灵组
                pass
            pass
        pass

    def checkCollide(self):
        '''碰撞检测'''
        #敌机与英雄子弹之间的碰撞检测
        collideDict = pygame.sprite.groupcollide(self.hero.bullets,self.enemy_group,True,False)
        if len(collideDict) > 0:
            for clist in collideDict.values():
                for x in clist:
                    x.isAlive = False
                    pass
                pass
            pass
        #英雄与敌机子弹之间的碰撞检测
        collidedBullets = pygame.sprite.spritecollide(self.hero,self.enemyBullets_group,True)
        if len(collidedBullets) > 0:
            self.hero.isAlive = False
            pass
        pass
    def update_sprites(self):
        '''精灵组的update和draw'''
        self.back_group.update()
        self.back_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.enemy_group.update()
        self.hero_group.draw(self.screen)
        self.hero_group.update()
        self.enemyBullets_group.update()
        self.enemyBullets_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)
        pass
    pass

if __name__ == '__main__':
    game = PlaneGame()
    game.startGame()
    