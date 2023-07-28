import pygame, random, os, sys
from pygame.constants import QUIT, K_DOWN, K_UP,K_LEFT,K_RIGHT, KEYDOWN, K_ESCAPE, K_c, K_q

pygame.init()
FPS = pygame.time.Clock()

######_Font_######
FONT = pygame.font.Font('font/Lugrasimo-Regular.ttf', 20)
######_Color_######

COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_RED = (255,0,0)
COLOR_GREEN = (0, 255,0)
COLOR_BLUE = (0,0,255)
COLOR_YELLOW = (233,201,17)

COLOR_GRAY = (212,212,212)
COLOR_BUTTON_HOVER = (135,0,0)

######_Menu_######

HEIGHT = 800
WIDTH = 1200

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

######_Resolution_######

HEIGHT = 800
WIDTH = 1200

######_Player_######
player = pygame.image.load('player/1-1.png').convert_alpha()
player_size = player.get_size()
# player = pygame.Surface(player_size)
# player.fill(COLOR_YELLOW)
player_rect = pygame.Rect(0, HEIGHT/2-50, *player_size)

IMAGE_PLAYER_PASS = 'player'
PLAYER_IMAGES = os.listdir(IMAGE_PLAYER_PASS)

PLAYER_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(PLAYER_IMAGE, 250)
image_player_index = 0

######_Move_######

# player_speed = [1, 1]
player_move_down = [0, 3]
player_move_right = [3, 0]
player_move_up = [0, -3]
player_move_left = [-3, 0]

######_Enemy_######
def create_enemy():
     enemy = pygame.image.load('enemy/1-1.png').convert_alpha()
     enemy_size = enemy.get_size()
     # enemy.fill(COLOR_RED)
     enemy_rect = pygame.Rect(WIDTH, random.randint(100,HEIGHT), *enemy_size)
     enemy_move = [random.randint(-5, -2),0]
     return [enemy, enemy_rect, enemy_move] 

IMAGE_ENEMY_PASS = 'enemy'
ENEMY_IMAGES = os.listdir(IMAGE_ENEMY_PASS)

PLAYER_IMAGE_ENEMY = pygame.USEREVENT + 4
pygame.time.set_timer(PLAYER_IMAGE_ENEMY, 150)
image_enemy_index = 0

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 2500)
enemies = []

######_Bonus_######
IMAGE_BONUS_PASS = 'bonus'
BONUS_IMAGES = os.listdir(IMAGE_BONUS_PASS)

def create_bonus():
     image_bonus_index = random.randint(0,3)
     bonus= pygame.image.load(os.path.join(IMAGE_BONUS_PASS,BONUS_IMAGES[image_bonus_index]))
     # bonus = pygame.image.load('img/bonus.png').convert_alpha()
     bonus_size = bonus.get_size()
     # bonus = pygame.Surface(bonus_size)
     # bonus.fill(COLOR_BLUE)
     bonus_rect = pygame.Rect(random.randint(60,WIDTH-200), -150, *bonus_size)
     bonus_move = [0,random.randint(1, 5)]
     return [bonus, bonus_rect, bonus_move] 

CREATE_BONUS = pygame.USEREVENT + 2 
pygame.time.set_timer(CREATE_BONUS, 1500)
bonuses = []

######_Health_######
HEALTH_PASS = 'health'
HEALTH_IMAGES = os.listdir(HEALTH_PASS)
health = 0
health_image = pygame.image.load(os.path.join(HEALTH_PASS,HEALTH_IMAGES[health]))

######__######_game_logic_######__######
playing = True

score = 0

bg = pygame.transform.scale(pygame.image.load('img/bg.jpg'),(WIDTH,HEIGHT))
bgx1 = 0
bgx2 = bg.get_width()
bg_move = 1

def paused():
     paused = True
     click = False
     while paused:
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
               if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                         pygame.quit()

          bg = pygame.transform.scale(pygame.image.load('img/main_menu_bg.jpg'),(WIDTH,HEIGHT))
          main_display.blit(bg,(0,0))

          draw_text(350, 150, "Paused", 150, 'font/Harrington.ttf', COLOR_BUTTON_HOVER)

          button_continue = button(WIDTH/2-90, 370, "Continue")
          button_menu = button(WIDTH/2-90, 470, "Main menu")
          button_quit = button(WIDTH/2-90, 570, "Quit")

          if button_continue.button_draw():
                paused = False
          if button_menu.button_draw():
                main_menu()
          if button_quit.button_draw():
                pygame.quit()
          
          pygame.display.update()
          FPS.tick(240)

def retry():
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
               if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                         pygame.quit()

          bg = pygame.transform.scale(pygame.image.load('img/main_menu_bg.jpg'),(WIDTH,HEIGHT))
          main_display.blit(bg,(0,0))

          draw_text(250, 150, "Game over", 150, 'font/Harrington.ttf', COLOR_BUTTON_HOVER)

          button_again = button(WIDTH/2-90, 370, "Retry")
          button_menu = button(WIDTH/2-90, 470, "Main menu")
          button_quit = button(WIDTH/2-90, 570, "Quit")

          if button_again.button_draw():
               game()
          if button_menu.button_draw():
               main_menu()
               playing = False
               
          if button_quit.button_draw():
               pygame.quit()
          
          pygame.display.update()
          FPS.tick(240)

def settings():
     status = ""
     while True:
          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
               if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                         pygame.quit()

          bg = pygame.transform.scale(pygame.image.load('img/main_menu_bg.jpg'),(WIDTH,HEIGHT))
          main_display.blit(bg,(0,0))

          draw_text(200, 150, "Levels of difficulty", 100, 'font/Harrington.ttf', COLOR_BUTTON_HOVER)

          button_easy = button(WIDTH/2-90, 370, "Easy")
          button_diff = button(WIDTH/2-90, 470, "Difficult")
          button_menu = button(WIDTH/2-90, 570, "Main menu")
          
          if button_easy.button_draw():
               pygame.time.set_timer(CREATE_ENEMY, 2500)
               pygame.time.set_timer(CREATE_BONUS, 1500)
               status = "Easy"
          if button_diff.button_draw():
               pygame.time.set_timer(CREATE_ENEMY, 500)
               pygame.time.set_timer(CREATE_BONUS, 3500)
               status = "Difficult"
          if button_menu.button_draw():
               main_menu()
          
          draw_text(WIDTH-180,HEIGHT-50,f'Difficult: {status}',20,'font/Harrington.ttf', COLOR_BUTTON_HOVER)
          pygame.display.update()
          FPS.tick(240)
 
def game():
     image_player_index = 0
     image_enemy_index = 0
     bgx1 = 0
     bgx2 = bg.get_width()
     player_rect = pygame.Rect(0, HEIGHT/2-50, *player_size)
     health = 0
     health_image = pygame.image.load(os.path.join(HEALTH_PASS,HEALTH_IMAGES[health]))
     score = 0
     player = pygame.image.load('player/1-1.png').convert_alpha()
     
     playing = True
     
     for enemy in enemies:
          enemies.clear()

          ######_Bonus_remover_######
     for bonus in bonuses:
          bonuses.clear()

     while playing:

               FPS.tick(240)
               for event in pygame.event.get():
                    if event.type == QUIT:
                         pygame.quit()
                         sys.exit()
                    if event.type == KEYDOWN:
                          if event.key == K_ESCAPE:
                              paused()
                    if event.type == CREATE_ENEMY:
                         enemies.append(create_enemy())
                    if event.type == CREATE_BONUS:
                         bonuses.append(create_bonus())
                    if event.type == PLAYER_IMAGE:
                         player = pygame.image.load(os.path.join(IMAGE_PLAYER_PASS,PLAYER_IMAGES[image_player_index]))
                         image_player_index += 1
                         if image_player_index >= len(PLAYER_IMAGES):
                              image_player_index = 0
                    if event.type == PLAYER_IMAGE_ENEMY:
                         for enemy in enemies:
                              enemy[0] = pygame.image.load(os.path.join(IMAGE_ENEMY_PASS,ENEMY_IMAGES[image_enemy_index]))
                              image_enemy_index += 1
                              if image_enemy_index >= len(ENEMY_IMAGES):
                                   image_enemy_index = 0


          #     main_display.fill(COLOR_BLACK)
               bgx1 -= bg_move
               bgx2 -= bg_move

               if bgx1 < -bg.get_width():
                    bgx1 = bg.get_width()
               if bgx2 < -bg.get_width():
                    bgx2 = bg.get_width()

               main_display.blit(bg, (bgx1,0))
               main_display.blit(bg, (bgx2,0))

          ######_Label_######
               font = pygame.font.Font('font/Lugrasimo-Regular.ttf', 20)
               label = FONT.render(f'Score: {score}', 1, COLOR_YELLOW)
               main_display.blit(label, (WIDTH-150, 40)) 
          ######_Health_######
               main_display.blit(health_image, (30,40)) 
          ######_Control_######
               keys = pygame.key.get_pressed()

               if keys[K_DOWN] and player_rect.bottom < HEIGHT:
                    player_rect = player_rect.move(player_move_down)

               if keys[K_UP] and player_rect.top >= 90:
                    player_rect = player_rect.move(player_move_up)      

               if keys[K_RIGHT] and player_rect.right < WIDTH:
                    player_rect = player_rect.move(player_move_right)

               if keys[K_LEFT] and player_rect.left >= 0:
                    player_rect = player_rect.move(player_move_left)

               
          ######_Enemy_move_######
          #   enemy_rect = enemy_rect.move(enemy_move)

               for enemy in enemies:
                    enemy[1] = enemy[1].move(enemy[2])
                    main_display.blit(enemy[0], enemy[1])
               
                    if player_rect.colliderect(enemy[1]):
                              health = health + 1
                              enemies.pop(enemies.index(enemy)) 
                              if health > 4:
                                  retry()
                              health_image = pygame.image.load(os.path.join(HEALTH_PASS,HEALTH_IMAGES[health]))

          ######_Bonus_move_######
          #   bonus_rect = bonus_rect.move(bonus_move)

               for bonus in bonuses:
                    bonus[1] = bonus[1].move(bonus[2])
                    main_display.blit(bonus[0], bonus[1])
               
                    if player_rect.colliderect(bonus[1]):
                         score = score + 1
                         bonuses.pop(bonuses.index(bonus)) 

               main_display.blit(player, player_rect) 
               pygame.display.flip()

          ######_Enemy_remover_######
               for enemy in enemies:
                    if enemy[1].left < 0:
                         enemies.pop(enemies.index(enemy))

          ######_Bonus_remover_######
               for bonus in bonuses:
                         if bonus[1].bottom > HEIGHT:
                              bonuses.pop(bonuses.index(bonus))
               pygame.display.update()

click = False

class button():
     button_col = COLOR_GRAY
     button_hover = COLOR_BUTTON_HOVER
     click_col = COLOR_GREEN
     text_col = COLOR_BLACK
     width = 200
     height = 40

     def __init__(self,x,y,text):
          self.x = x
          self.y = y
          self.text = text

     def button_draw(self):
          global click 
          action = False

          pos = pygame.mouse.get_pos()
          button_rect = pygame.Rect(self.x, self.y, self.width, self.height)
          
          if button_rect.collidepoint(pos):
               if pygame.mouse.get_pressed()[0] == 1:
                    click = True
               elif pygame.mouse.get_pressed()[0] == 0 and click == True:
                    click = False
                    action = True
               else:
                    pygame.draw.rect(main_display, self.button_hover, button_rect)
          else:
               pygame.draw.rect(main_display,self.button_col,button_rect)
          
          label = FONT.render(self.text, 1, self.text_col)
          label_len = label.get_width()
          main_display.blit(label, (self.x + int(self.width / 2) - int(label_len / 2), self.y + 5))
          
          return action

def draw_text(x,y,text,size,font,col):
     FONT = pygame.font.Font(font, size)
     label = FONT.render(text, 1, col)
     main_display.blit(label, (int(x), y))
    
def main_menu():
    click = False
    button_game = button(WIDTH/2-100, 390, "Start")
    button_diff = button(WIDTH/2-100, 490, "Difficulty")
    button_quit = button(WIDTH/2-100, 590, "Quit")

    while True:
          FPS.tick(240)
          bg = pygame.transform.scale(pygame.image.load('img/main_menu_bg.jpg'),(WIDTH,HEIGHT))
          main_display.blit(bg,(0,0))

          title_bg = pygame.image.load('img/title_bg_border.png')
          main_display.blit(title_bg,(330,-40))
          draw_text(250, 150, "New Game", 150, 'font/Harrington.ttf', COLOR_BUTTON_HOVER)

          if button_game.button_draw():
                          game()
          if button_diff.button_draw():
                          settings()
          if button_quit.button_draw():
                          pygame.quit()

          for event in pygame.event.get():
               if event.type == QUIT:
                    pygame.quit()
               if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                         pygame.quit()
                         sys.exit()
               if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                         click = True
          pygame.display.update()
     

main_menu()
pygame.display.quit()     

