import sys

import pygame

import tanks


def main():
    pygame.init()
    pygame.display.set_caption("Tank War    -yangbin")
    pygame.mixer.init()
    screen = pygame.display.set_mode((630, 630))
    is_gameover = False
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/simkai.ttf',80)
    grade = [0,0]
    is_move = False
    p1_is_move = False
    p2_is_move = False

    # 加载音效
    start_sound = pygame.mixer.Sound("./audios/start.wav")
    start_sound.set_volume(0.5)
    fire_sound = pygame.mixer.Sound("./audios/fire.wav")
    Gunfire_sound = pygame.mixer.Sound("./audios/Gunfire.wav")
    add_sound = pygame.mixer.Sound("./audios/add.wav")
    bang_sound = pygame.mixer.Sound("./audios/bang.wav")

    while not is_gameover:
        tanksGroup = pygame.sprite.Group()
        bulletGroup = pygame.sprite.Group()
        tank_player1 = tanks.myTank(1)
        tank_player2 = tanks.myTank(2)
        tanksGroup.add(tank_player1)
        tanksGroup.add(tank_player2)
        add_sound.play()
        # 轮胎动画效果
        time = 0
        is_switch_tank = False
        while True:
            screen.fill(1)

            # 绘制比分
            gradeText = font.render(str(grade[0]) + " : " + str(grade[1]),True,(0,0xff,0xf0))
            gradeRect = gradeText.get_rect()
            screenRect = screen.get_rect()
            gradeRect.center = screenRect.center
            screen.blit(gradeText,(gradeRect.left,40))
           
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            time += 1
            if time == 5:
                time = 0
                is_switch_tank = not is_switch_tank
            # 检查用户键盘操作
            key_pressed = pygame.key.get_pressed()

            # AI 操控玩家一
            # tanksGroup.remove(tank_player1)
            # tank_player1.AI(tank_player2.bullet,tank_player2,tanksGroup,Gunfire_sound)
            # tanksGroup.add(tank_player1)

            # 玩家一
            # WSAD -> 上下左右
            # 空格键射击
            if key_pressed[pygame.K_w]:
                tanksGroup.remove(tank_player1)
                p1_is_move = tank_player1.move_up(tanksGroup)    
                tanksGroup.add(tank_player1)
            elif key_pressed[pygame.K_s]:
                tanksGroup.remove(tank_player1)
                p1_is_move = tank_player1.move_down(tanksGroup)
                tanksGroup.add(tank_player1)
            elif key_pressed[pygame.K_a]:
                tanksGroup.remove(tank_player1)
                p1_is_move = tank_player1.move_left(tanksGroup)
                tanksGroup.add(tank_player1)
            elif key_pressed[pygame.K_d]:
                tanksGroup.remove(tank_player1)
                p1_is_move = tank_player1.move_right(tanksGroup)
                tanksGroup.add(tank_player1)
            elif key_pressed[pygame.K_SPACE]:
                if not tank_player1.bullet.being:
                    tank_player1.shoot()
                    fire_sound.play()

            # AI 操控
            tanksGroup.remove(tank_player2)
            tank_player2.AI(tank_player1.bullet,tank_player1,tanksGroup,Gunfire_sound)
            tanksGroup.add(tank_player2)
            
            # # 玩家二 操控
            # # ↑↓←→ -> 上下左右
            # # 小键盘0键射击
            # if key_pressed[pygame.K_UP]:
            #     tanksGroup.remove(tank_player2)
            #     p2_is_move = tank_player2.move_up(tanksGroup)
            #     tanksGroup.add(tank_player2)
            # elif key_pressed[pygame.K_DOWN]:
            #     tanksGroup.remove(tank_player2)
            #     p2_is_move = tank_player2.move_down(tanksGroup)
            #     tanksGroup.add(tank_player2)
            # elif key_pressed[pygame.K_LEFT]:
            #     tanksGroup.remove(tank_player2)
            #     p2_is_move = tank_player2.move_left(tanksGroup)
            #     tanksGroup.add(tank_player2)
            # elif key_pressed[pygame.K_RIGHT]:
            #     tanksGroup.remove(tank_player2)
            #     p2_is_move = tank_player2.move_right(tanksGroup)
            #     tanksGroup.add(tank_player2)
            # elif key_pressed[pygame.K_RSHIFT]:
            #     if not tank_player2.bullet.being:
            #         tank_player2.shoot()
            
            if is_switch_tank and p1_is_move:
                screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
                p1_is_move = False
            else:
                screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
                
            if is_switch_tank and p2_is_move:
                screen.blit(tank_player2.tank_1, (tank_player2.rect.left, tank_player2.rect.top))
                p2_is_move = False
            else:
                screen.blit(tank_player2.tank_0, (tank_player2.rect.left, tank_player2.rect.top))

            # 子弹
            for tank in tanksGroup:
                if tank.bullet.being:
                    tank.bullet.move()
                    screen.blit(tank.bullet.bullet,tank.bullet.rect)
                   
            #判断子弹和子弹是否碰撞(子弹都存在的情况下才会碰撞)
            if  tank_player1.bullet.being == True and tank_player2.bullet.being == True and pygame.sprite.collide_rect(tank_player1.bullet,tank_player2.bullet):
                tank_player1.bullet.being = False
                tank_player2.bullet.being = False
            
            #判断子弹和坦克是否相撞           
            if tank_player1.bullet.being and pygame.sprite.collide_rect(tank_player1.bullet,tank_player2):
                tank_player1.bullet.being = False
                grade[0] += 1
                bang_sound.play()
                break
            if tank_player2.bullet.being and pygame.sprite.collide_rect(tank_player2.bullet,tank_player1):
                tank_player2.bullet.being = False
                grade[1] += 1
                bang_sound.play()
                break

            pygame.display.flip()
            clock.tick(60)
        print("game over")

if __name__ == "__main__":
    main()
