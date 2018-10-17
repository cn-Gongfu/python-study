import math
import random

import pygame
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()

size = width,height = 640,480
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rabbit -- yangbin")

keys = [False,False,False,False]# 玩家按键
mousestate = False
playerpos = [100,100] #玩家位置
acc = [0,0]
arrows = [] # 箭
badtimer, healthvalue = 0,194
badguys = [[640,100]]
running, exitcode = True, False
badguyscount, badguysspeed = 3,7

# 添加资源
rabbit_img = pygame.image.load("images/dude.png")
rabbit_img2 = pygame.image.load("images/dude2.png")
grass_img = pygame.image.load("images/grass.png")
castle_img = pygame.image.load("images/castle.png")
arrow_img = pygame.image.load("images/bullet.png")
badguys_img = pygame.image.load("images/badguy.png")
badguys_img2 = pygame.image.load("images/badguy2.png")
badguys_img3 = pygame.image.load("images/badguy3.png")
badguys_img4 = pygame.image.load("images/badguy4.png")
healthbar_img = pygame.image.load("images/healthbar.png")
health_img = pygame.image.load("images/health.png")
gameover_img  = pygame.image.load("images/gameover.png")
youwin_img = pygame.image.load("images/youwin.png")

# 加载声音文件并配置
pygame.mixer.music.load('audio/moonlight.wav')
hit = pygame.mixer.Sound("audio/explode.wav")
enemy = pygame.mixer.Sound("audio/enemy.wav")
shoot = pygame.mixer.Sound("audio/shoot.wav")
hit.set_volume(0.05)
enemy.set_volume(0.05)
shoot.set_volume(0.05)

#背景音乐循环播放
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.25)

while running:
    screen.fill(0)
    for x in range(width//grass_img.get_width()+1):
        for y in range(height//grass_img.get_height()+1):
            screen.blit(grass_img,(x*100,y*100))
    screen.blit(castle_img,(0,30))
    screen.blit(castle_img,(0,135))
    screen.blit(castle_img,(0,240))
    screen.blit(castle_img,(0,345))
    # 获取鼠标和玩家的位置,然后通过atan函数得出角度和弧度
    # 当兔子被旋转的时候,它的位置将会改变,计算兔子新的位置,在屏幕上显示出来
    position = pygame.mouse.get_pos()
    angle = math.atan2(position[1]-(playerpos[1]+32),position[0]-(playerpos[0]+26))
    if not mousestate:
        rabbit = rabbit_img
    else:
        rabbit = rabbit_img2
    playerrot = pygame.transform.rotate(rabbit,360-angle*57.29)
    playerpos1 = (playerpos[0]-playerrot.get_rect().width/2,playerpos[1]-playerrot.get_rect().height/2)
    screen.blit(playerrot, playerpos1)
    # print(playerrot.get_rect().width,playerrot.get_rect().height)
    
    # 画箭头
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1] += velx
        bullet[2] += vely
        if bullet[1] < -64 or bullet[1]>640 or bullet[2]<-64 or bullet[2]>480:
            arrows.pop(index)
        index += 1
        for arrow in arrows:
            arrow1 = pygame.transform.rotate(arrow_img,360-arrow[0]*57.29)
            screen.blit(arrow1,(arrow[1],arrow[2]))

    # 创造敌人
    if badtimer < badguyscount:
        badguys.append([640, random.randint(50,430)])
        badtimer += 1

    index_badguy = 0
    for badguy in badguys:
        if badguy[0] < -64:
            badguys.pop(index_badguy)
        badguy[0] -= badguysspeed
        badrect = pygame.Rect(badguys_img.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64: # 敌人进入城堡
            hit.play()
            badguys.pop(index_badguy)
            healthvalue -= random.randint(5,20)
        
        badtimer = len(badguys)
        index_arrow = 0
        for bullet in arrows:
            bulletrect = pygame.Rect(arrow_img.get_rect())
            bulletrect.left = bullet[1]
            bulletrect.top = bullet[2]
            if badrect.colliderect(bulletrect):
                enemy.play()
                badguys.pop(index_badguy)
                arrows.pop(index_arrow)
                acc[0] += 1
            index_arrow += 1
        index_badguy += 1

    for badguy in badguys:
        badguyimg = None
        p = 20 # 步伐速度
        x = math.fabs(badguy[0] % 20)
        if x < p * 0.25:
            badguyimg = badguys_img
        elif x < p * 0.5:
            badguyimg = badguys_img2
        elif x < p * 0.75:
            badguyimg = badguys_img3
        elif x < p:
            badguyimg = badguys_img4
        screen.blit(badguyimg, badguy)

    #血条
    screen.blit(healthbar_img,(5,5))
    for health in range(healthvalue):
        screen.blit(health_img,(health+8,8))

    font = pygame.font.Font(None,24)
    killtext = font.render("kill:" + str(acc[0]) + " fps:" + str(int(clock.get_fps())),True,(255,0,0))
    textrect = killtext.get_rect()
    textrect.topright=[635,5]
    tiptext = font.render("kill 100 win",True,(0,255,0))
    screen.blit(tiptext,(300,5))
    font = pygame.font.Font(None,16)
    ps1text = font.render(u"1.enemy +1" ,True,(0,255,0))
    ps2text = font.render(u"2.enemy -1" ,True,(0,255,0))
    ps3text = font.render(u"3.speed +1" ,True,(0,255,0))
    ps4text = font.render(u"4.speed -1" ,True,(0,255,0))
    screen.blit(ps1text,(560,380))
    screen.blit(ps2text,(560,404))
    screen.blit(ps3text,(560,428))
    screen.blit(ps4text,(560,452))
    
    screen.blit(killtext,textrect)

    # 更新屏幕
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == K_w:
                keys[0] = True
            elif event.key == K_a:
                keys[1] = True
            elif event.key == K_s:
                keys[2] = True
            elif event.key == K_d:
                keys[3] = True
            elif event.key == K_1:
                badguyscount += 1
            elif event.key == K_2:
                if badguyscount >= 1: badguyscount -= 1
            elif event.key == K_3:
                badguysspeed += 1
            elif event.key == K_4:
                if badguysspeed >=1: badguysspeed -= 1

        if event.type == pygame.KEYUP:
            if event.key == K_w:
                keys[0] = False
            elif event.key == K_a:
                keys[1] = False
            elif event.key == K_s:
                keys[2] = False
            elif event.key == K_d:
                keys[3] = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousestate = True
            shoot.play()
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos1[1]+32), position[0]-(playerpos1[0]+26)),
						   playerpos1[0]+32, playerpos1[1]+26])
        if event.type == pygame.MOUSEBUTTONUP:
            mousestate = False

    if keys[0]:
        playerpos[1] -= 5
    elif keys[2]:
        playerpos[1] += 5
    if keys[1]:
        playerpos[0] -= 5
    elif keys[3]:
        playerpos[0] += 5

    clock.tick(30) # 帧率限制

    #判断失败
    if healthvalue < 0:
        running = False
        exitcode = False

    # 杀敌数超过100 成功
    if acc[0] > 100: 
        running = False
        exitcode = True

accuracy = 0
if acc[1] != 0:
    accuracy = acc[0]/acc[1] * 100
    accuracy = ("%.2f" % accuracy)

if exitcode:
    pygame.font.init()
    font = pygame.font.Font(None,24)
    text = font.render("Accuracy"+str(accuracy)+"%",True,(255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(youwin_img,(0,0))
    screen.blit(text,textRect)
else:
    pygame.font.init()
    font = pygame.font.Font(None,24)
    text = font.render("Accuracy  "+str(accuracy)+"%",True,(255,0,0))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery+24
    screen.blit(gameover_img,(0,0))
    screen.blit(text,textRect)

while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			exit()
	pygame.display.flip()
