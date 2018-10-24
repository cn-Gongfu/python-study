# 坦克
import pygame,random,bullet,math,random

class myTank(pygame.sprite.Sprite):
    def __init__(self,player):
        pygame.sprite.Sprite.__init__(self)
        #玩家编号
        self.player = player
        #不同的玩家用不同的坦克(不同的等级对应不同的图)
        if player == 1:
            self.tanks = ["./images/myTank/tank_T1_0.png","./images/myTank/tank_T1_1.png","./images/myTank/tank_T1_2.png"]
        elif player == 2:
            self.tanks = ["./images/myTank/tank_T2_0.png","./images/myTank/tank_T2_1.png","./images/myTank/tank_T2_2.png"]
        else:
            raise ValueError("myTank class -> palyer value error")

        #坦克等级
        self.level = 0
        #载入
        self.tank = pygame.image.load(self.tanks[self.level]).convert_alpha()
        self.tank_0 = self.tank.subsurface((0,0),(48,48))
        self.tank_1 = self.tank.subsurface((0,48),(48,48))
        self.rect = self.tank_0.get_rect()
        #坦克方向
        self.direction_x, self.direction_y = 0,-1
        #不同玩家出生的位置
        if player == 1:
            self.rect.left, self.rect.top = 3 + 24 * 8, 3 + 24 * 24
        if player == 2:
            self.rect.left, self.rect.top = 3 + 24 * 12, 3 + 24 * 4
        #坦克速度
        self.speed = 3
        #是否存活
        self.being = True
        #有几条命
        self.life = 3
        # 子弹
        self.bullet = bullet.Bullet()
        # 轨迹
        self.track = 0
        # 是否满足射击条件
        self.is_shoot = False
    
    # 射击
    def shoot(self):
        self.bullet.being = True
        self.bullet.turn(self.direction_x,self.direction_y)
        # 根据子弹方向,调整子弹位置
        if self.direction_x == 0 and self.direction_y == -1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.bottom = self.rect.top - 1
        elif self.direction_x == 0 and self.direction_y == 1:
            self.bullet.rect.left = self.rect.left + 20
            self.bullet.rect.top = self.rect.bottom + 1
        elif self.direction_x == -1 and self.direction_y == 0:
            self.bullet.rect.right = self.rect.left - 1
            self.bullet.rect.top = self.rect.top + 20
        elif self.direction_x == 1 and self.direction_y == 0:
            self.bullet.rect.left = self.rect.right + 1
            self.bullet.rect.top = self.rect.top + 20
        else:
            raise ValueError('myTank class -> direction value error.')

    def move_up(self,tanksGroup):
        self.direction_x,self.direction_y = 0,-1
        self.rect = self.rect.move(self.speed*self.direction_x,self.speed*self.direction_y)
        is_move = True
        self.tank_0 = self.tank.subsurface((0, 0), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 0), (48, 48))
		# 地图顶端
        if self.rect.top < 3:
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        # 与其他坦克发生碰撞
        if pygame.sprite.spritecollide(self,tanksGroup,False,None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False

        return is_move
    
    def move_down(self,tanksGroup):
        self.direction_x,self.direction_y = 0,1
        self.rect = self.rect.move(self.speed*self.direction_x,self.speed*self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 48), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48), (48, 48))
        is_move = True
        if self.rect.bottom > 630-3:
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        # 与其他坦克发生碰撞
        if pygame.sprite.spritecollide(self,tanksGroup,False,None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False

        return is_move

    def move_left(self,tanksGroup):
        self.direction_x,self.direction_y = -1,0
        self.rect = self.rect.move(self.speed*self.direction_x,self.speed*self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 96), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 96), (48, 48))
        is_move = True
        if self.rect.left < 3:
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        # 与其他坦克发生碰撞
        if pygame.sprite.spritecollide(self,tanksGroup,False,None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False

        return is_move

    def move_right(self,tanksGroup):
        self.direction_x,self.direction_y = 1,0
        self.rect = self.rect.move(self.speed*self.direction_x,self.speed*self.direction_y)
        self.tank_0 = self.tank.subsurface((0, 48*3), (48, 48))
        self.tank_1 = self.tank.subsurface((48, 48*3), (48, 48))
        is_move = True
        if self.rect.left > 630 - 51:
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False
        # 与其他坦克发生碰撞
        if pygame.sprite.spritecollide(self,tanksGroup,False,None):
            self.rect = self.rect.move(self.speed*-self.direction_x, self.speed*-self.direction_y)
            is_move = False

        return is_move
    
    def AI(self,bullet,tank,tanksGroup,Gunfire_sound):
        pass
        # 判断是否收到子弹袭击
        tx = tank.rect.x
        ty = tank.rect.y

        sx = self.rect.x
        sy = self.rect.y

        distx = sx - tx
        disty = sy - ty

        bx = bullet.rect.x
        by = bullet.rect.y
        
        sbx = sx - bx
        sby = sy - by
        # 如果敌人发射炮弹  躲避攻击
        if bullet.being:
            # y 方向受到攻击
            if sbx < 20 and sbx > -48:
                if sbx < -34:
                    self.track = 1
                else:
                    self.track = 2
            # x 反向收到攻击
            elif sby < 20 and sby > -48:
                if sby < -34:
                    self.track = 3
                else:
                    self.track = 4
            
        else:
            # 没有受到攻击           
            if not self.bullet.being:
                 # 如果有炮弹 找位置发射
                # 目标位置
                # 距离目标哪个轴距最短, 向哪个方向移动
                if abs(disty) < abs(distx):
                    if disty > 20:
                        self.track = 3
                    elif disty < -20:
                        self.track = 4        
                else:
                    if distx > 20:
                        self.track = 1
                    elif distx < -20:
                        self.track = 2

                # 计算目标方向 发射炮弹
                if abs(disty) <= 24:
                    if distx > 0:
                        self.track = 1
                    else:
                        self.track = 2
                    self.is_shoot = True
                elif abs(distx) <= 24:
                    if disty > 0:
                        self.track = 3
                    else:
                        self.track = 4
                    self.is_shoot = True
            else:
                if abs(disty) > abs(distx):
                    if distx > 0:
                        self.track = 2
                    else:
                        self.track = 1
                else:
                    if disty > 0:
                        self.track = 4
                    else:
                        self.track = 3


                

        if self.track == 1:
            self.move_left(tanksGroup)
        elif self.track == 2:
            self.move_right(tanksGroup)
        elif self.track == 3:
            self.move_up(tanksGroup)
        elif self.track == 4:
            self.move_down(tanksGroup)
        
        if self.is_shoot:
            if not self.bullet.being:
                self.shoot()
                Gunfire_sound.play()
            self.is_shoot = False
        