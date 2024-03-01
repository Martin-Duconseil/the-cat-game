
# The Cat Game - Snake alternative

# --------| Import |---------- #

import pygame, sys, random
from pygame.math import Vector2
from button import Button

# --------| Class CAT |---------- #

class cat:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        # Graphics

        self.head_up = pygame.image.load('the cat game/graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('the cat game/graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('the cat game/graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('the cat game/graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('the cat game/graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('the cat game/graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('the cat game/graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('the cat game/graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('the cat game/graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('the cat game/graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('the cat game/graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('the cat game/graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('the cat game/graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('the cat game/graphics/body_bl.png').convert_alpha()

        # Sound

        self.crunch_sound = pygame.mixer.Sound('the cat game/sound/crunch.wav')
    
    # Draw the cat on the screen

    def draw_cat(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index,block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)

            # Direction of the head and tail

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)  
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl,block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl,block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr,block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br,block_rect)

    # Update the head graphics

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.head_left
        elif head_relation == Vector2(-1,0): self.head = self.head_right
        elif head_relation == Vector2(0,1): self.head = self.head_up
        elif head_relation == Vector2(0,-1): self.head = self.head_down

    # Update the tail graphics

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0): self.tail = self.tail_right
        elif tail_relation == Vector2(0,1): self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1): self.tail = self.tail_down

    # Move the cat - Directions

    def move_cat(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:    
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    # Add a block to the cat

    def add_block(self):
        self.new_block = True

    # Play the crunch sound

    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Reset the cat

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

# --------| Class FOOD |---------- #

class food:
    def __init__(self):
        self.randomize()
    
    # Draw the food on the screen

    def draw_food(self):
        if self.food_type == "fish":
            food_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(fish, food_rect)
        elif self.food_type == "steak":
            food_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
            screen.blit(steak, food_rect)

    # Randomize the food position

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)
        self.food_type = random.choice(["fish", "steak"])


# --------| Class MAIN |---------- #

class MAIN:
    def __init__(self):
        self.cat = cat()
        self.food = food()

    def update(self):
        self.cat.move_cat()
        self.check_collision()
        self.check_fail()
    
    def draw_elements(self):
        self.draw_ground()
        self.food.draw_food()
        self.cat.draw_cat()
        self.draw_score()

    def check_collision(self):
        if self.food.pos == self.cat.body[0]:
          self.food.randomize()
          self.cat.add_block()
          self.cat.play_crunch_sound()
        
        for block in self.cat.body[1:]:
            if block == self.food.pos:
                self.food.randomize()

    def check_fail(self):
        if not 0 <= self.cat.body[0].x < cell_number or not 0 <= self.cat.body[0].y < cell_number:
            self.game_over()
        
        for block in self.cat.body[1:]:
            if block == self.cat.body[0]:
                self.game_over()
     
            
    def game_over(self):
        self.cat.reset()

    # Draw the tiles on the ground

    def draw_ground(self):
        ground_color = (37,37,37)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        ground_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,ground_color,ground_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        ground_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
                        pygame.draw.rect(screen,ground_color,ground_rect)

    # Draw the score on the screen

    def draw_score(self):
        score_text = str(len(self.cat.body) - 3)
        score_surface = game_font.render(score_text,True,(129,79,22))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        fish_rect = fish.get_rect(midright = (score_rect.left,score_rect.centery))
        bg_rect = pygame.Rect(fish_rect.left,fish_rect.top,fish_rect.width + score_rect.width + 10,fish_rect.height)

        pygame.draw.rect(screen,(250,250,250),bg_rect)
        screen.blit(score_surface,score_rect)
        screen.blit(fish,fish_rect)
        pygame.draw.rect(screen,(129,79,22),bg_rect,2)

# --------| Pygame INIT |---------- #

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

# --------| Display |---------- #

cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock() # Clock to limit the frame rate
fish = pygame.image.load('the cat game/graphics/fish.png').convert_alpha()
steak = pygame.image.load('the cat game/graphics/steak.png').convert_alpha()
game_font = pygame.font.Font('the cat game/font/days-one.regular.ttf',25)

SCREEN = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))

BG = pygame.image.load('the cat game/graphics/background_main_menu.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

def get_font(size): 
    return pygame.font.Font("the cat game/font/days-one.regular.ttf", size)

main_game = MAIN()

# --------| Play Loop |---------- #

def play():
    pygame.display.set_caption('Play')

    while True:
        
        # Draw all our elements (Background, cat, food, score, etc.)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if main_game.cat.direction.y != 1:
                        main_game.cat.direction = Vector2(0,-1)
                if event.key == pygame.K_RIGHT:
                    if main_game.cat.direction.x != -1:
                        main_game.cat.direction = Vector2(1,0)        
                if event.key == pygame.K_DOWN:
                    if main_game.cat.direction.y != -1:
                        main_game.cat.direction = Vector2(0,1)
                if event.key == pygame.K_LEFT:
                    if main_game.cat.direction.x != 1:
                        main_game.cat.direction = Vector2(-1,0)
                if event.key == pygame.K_ESCAPE:
                    main_game.game_over()
                    main_menu()
                
        # Gray background
                    
        screen.fill((72,72,72))

        # Draw the elements

        main_game.draw_elements()
        pygame.display.update()

        # Limit the frame rate to 60 fps

        clock.tick(60) 
    
        pygame.display.update()

# --------| Main Menu |---------- #

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("the cat game/graphics/Play Rect.png"), pos=(550, 350), 
                            text_input="Play", font=get_font(60), base_color="#252525", hovering_color="#252525")
        QUIT_BUTTON = Button(image=pygame.image.load("the cat game/graphics/Quit Rect.png"), pos=(550, 550), 
                            text_input="Quit", font=get_font(60), base_color="#252525", hovering_color="#252525")
        
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
