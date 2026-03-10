import pygame
import random
import sys
from pygame.math import Vector2

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()

#color
black = (20, 20, 20)
golden_yellow = (255, 200, 90)
green = (120, 220, 120)
cream = (230, 220, 200)
light_brown = (130, 70, 25)
dark_brown = (92, 45, 18)
white = (255, 255, 255)
red = (213, 50, 80)
dark_green = (34, 139, 34)

#game-screen
screen_width = 15
screen_height = 15
cell_size = 40

game_window = pygame.display.set_mode(
    (screen_width * cell_size, screen_height * cell_size)
)
pygame.display.set_caption("Caterpillar")

clock = pygame.time.Clock()
fps = 90

#font
game_font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 28)

#time
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

#graphics
leaf_1 = pygame.transform.scale(pygame.image.load("graphics/leaf_1.png").convert_alpha(), (cell_size, cell_size))
leaf_2 = pygame.transform.scale(pygame.image.load("graphics/leaf_2.png").convert_alpha(), (cell_size, cell_size))
leaf_3 = pygame.transform.scale(pygame.image.load("graphics/leaf_3.png").convert_alpha(), (cell_size, cell_size))
leaf_4 = pygame.transform.scale(pygame.image.load("graphics/leaf_4.png").convert_alpha(), (cell_size, cell_size))
apple = pygame.transform.scale(pygame.image.load("graphics/apple.png").convert_alpha(), (cell_size, cell_size))
pea = pygame.transform.scale(pygame.image.load("graphics/pea.png").convert_alpha(), (cell_size, cell_size))
vegetable = pygame.transform.scale(pygame.image.load("graphics/vegetable.png").convert_alpha(), (cell_size, cell_size))

food = [leaf_1, leaf_2, leaf_3, leaf_4, apple, pea, vegetable]


#game-state
state_menu = "menu"
state_playing = "playing"
state_paused = "paused"
state_game_over = "game_over"

#caterpillar
class Caterpillar:
    def __init__(self):
        self.reset()

        #head
        self.head_up = pygame.transform.scale(pygame.image.load("Graphics/head_up.png").convert_alpha(), (cell_size, cell_size))
        self.head_down = pygame.transform.scale(pygame.image.load("Graphics/head_down.png").convert_alpha(), (cell_size, cell_size))
        self.head_left = pygame.transform.scale(pygame.image.load("Graphics/head_left.png").convert_alpha(), (cell_size, cell_size))
        self.head_right = pygame.transform.scale(pygame.image.load("Graphics/head_right.png").convert_alpha(), (cell_size, cell_size))

        #tail
        self.tail_up = pygame.transform.scale(pygame.image.load("Graphics/tail_up.png").convert_alpha(), (cell_size, cell_size))
        self.tail_down = pygame.transform.scale(pygame.image.load("Graphics/tail_down.png").convert_alpha(), (cell_size, cell_size))
        self.tail_left = pygame.transform.scale(pygame.image.load("Graphics/tail_left.png").convert_alpha(), (cell_size, cell_size))
        self.tail_right = pygame.transform.scale(pygame.image.load("Graphics/tail_right.png").convert_alpha(), (cell_size, cell_size))

        #body
        self.body_vertical = pygame.transform.scale(pygame.image.load("Graphics/body_vertical.png").convert_alpha(), (cell_size, cell_size))
        self.body_horizontal = pygame.transform.scale(pygame.image.load("Graphics/body_horizontal.png").convert_alpha(), (cell_size, cell_size))
        self.body_tl = pygame.transform.scale(pygame.image.load("Graphics/body_tl.png").convert_alpha(), (cell_size, cell_size))
        self.body_tr = pygame.transform.scale(pygame.image.load("Graphics/body_tr.png").convert_alpha(), (cell_size, cell_size))
        self.body_bl = pygame.transform.scale(pygame.image.load("Graphics/body_bl.png").convert_alpha(), (cell_size, cell_size))
        self.body_br = pygame.transform.scale(pygame.image.load("Graphics/body_br.png").convert_alpha(), (cell_size, cell_size))

        #sound
        self.chomp_sound = pygame.mixer.Sound("sound/chomp.wav")
        self.gameover_sound = pygame.mixer.Sound("sound/game-over.wav")

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw(self):
        self.update_head()
        self.update_tail()

        for i, block in enumerate(self.body):
            rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            if i == 0:
                game_window.blit(self.head, rect)
            elif i == len(self.body) - 1:
                game_window.blit(self.tail, rect)
            else:
                prev = self.body[i + 1] - block
                next = self.body[i - 1] - block

                if prev.x == next.x:
                    game_window.blit(self.body_vertical, rect)
                elif prev.y == next.y:
                    game_window.blit(self.body_horizontal, rect)
                else:
                    if prev.x == -1 and next.y == -1 or prev.y == -1 and next.x == -1:
                        game_window.blit(self.body_tl, rect)
                    elif prev.x == -1 and next.y == 1 or prev.y == 1 and next.x == -1:
                        game_window.blit(self.body_bl, rect)
                    elif prev.x == 1 and next.y == -1 or prev.y == -1 and next.x == 1:
                        game_window.blit(self.body_tr, rect)
                    elif prev.x == 1 and next.y == 1 or prev.y == 1 and next.x == 1:
                        game_window.blit(self.body_br, rect)

    def update_head(self):
        relation = self.body[1] - self.body[0]
        if relation == Vector2(1, 0):
            self.head = self.head_left
        elif relation == Vector2(-1, 0):
            self.head = self.head_right
        elif relation == Vector2(0, 1):
            self.head = self.head_up
        elif relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail(self):
        relation = self.body[-2] - self.body[-1]
        if relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move(self):
        if self.new_block:
            body = self.body[:]
            body.insert(0, body[0] + self.direction)
            self.body = body
            self.new_block = False
        else:
            body = self.body[:-1]
            body.insert(0, body[0] + self.direction)
            self.body = body

    def grow(self):
        self.new_block = True
        self.chomp_sound.play()


#fruit
class Fruit:
    def __init__(self, caterpillar_body=None):
        self.randomize(caterpillar_body)

    def randomize(self, caterpillar_body=None):
        max_attempts = 1000  
        attempts = 0
        
        while attempts < max_attempts:
            self.x = random.randint(0, screen_width - 1)
            self.y = random.randint(1, screen_height - 1)
            self.pos = Vector2(self.x, self.y)
            
            #Check if position is not inside caterpillar body
            if caterpillar_body is None or self.pos not in caterpillar_body:
                break
            
            attempts += 1
        
        self.image = random.choice(food)

    def draw(self):
        rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        game_window.blit(self.image, rect)


#main game
class Main:
    def __init__(self):
        self.caterpillar = Caterpillar()
        self.fruit = Fruit(self.caterpillar.body)  #Pass body to avoid spawning inside
        self.state = state_menu
        self.high_score = 0

    def update(self):
        if self.state != state_playing:
            return
        self.caterpillar.move()
        self.check_collision()
        self.check_fail()

    def draw(self):
        if self.state == state_menu:
            self.draw_menu()
        else:
            self.draw_background()
            self.fruit.draw()
            self.caterpillar.draw()
            self.draw_score()
            
            if self.state == state_paused:
                self.draw_paused()
            elif self.state == state_game_over:
                self.draw_game_over()

    def check_collision(self):
        if self.caterpillar.body[0] == self.fruit.pos:
            self.fruit.randomize(self.caterpillar.body)  
            self.caterpillar.grow()
            #Update high score
            current_score = (len(self.caterpillar.body) - 3) * 10
            if current_score > self.high_score:
                self.high_score = current_score

    def check_fail(self):
        head = self.caterpillar.body[0]
        if not (0 <= head.x < screen_width and 0 < head.y < screen_height):
            self.caterpillar.gameover_sound.play()
            self.state = state_game_over
            return

        for block in self.caterpillar.body[1:]:
            if block == head:
                self.caterpillar.gameover_sound.play()
                self.state = state_game_over
                return

    def start_game(self):
        #Start a new game from menu
        self.caterpillar.reset()
        self.fruit.randomize(self.caterpillar.body) 
        self.state = state_playing

    def reset_game(self):
        #Reset game after game over
        self.caterpillar.reset()
        self.fruit.randomize(self.caterpillar.body) 
        self.state = state_playing

    def toggle_pause(self):
        #Toggle pause state#
        if self.state == state_playing:
            self.state = state_paused
        elif self.state == state_paused:
            self.state = state_playing

    def go_to_menu(self):
        #Return to main menu#
        self.state = state_menu

    def draw_menu(self):
        #Draw main menu screen
        window_width = screen_width * cell_size
        window_height = screen_height * cell_size
        
        #Background
        game_window.fill(dark_brown)
        
        #Draw decorative background pattern
        for row in range(screen_height):
            for col in range(screen_width):
                if (row + col) % 2 == 0:
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(game_window, light_brown, rect)
        
        #Semi-transparent overlay for better text visibility
        overlay = pygame.Surface((window_width, window_height))
        overlay.set_alpha(150)
        overlay.fill(black)
        game_window.blit(overlay, (0, 0))

        #Title
        title_text = title_font.render("CATERPILLAR", True, dark_green)
        title_rect = title_text.get_rect(center=(window_width // 2, window_height // 2 - 120))
        game_window.blit(title_text, title_rect)

        #Subtitle
        subtitle_text = big_font.render("The Hungry Bug Game", True, green)
        subtitle_rect = subtitle_text.get_rect(center=(window_width // 2, window_height // 2 - 70))
        game_window.blit(subtitle_text, subtitle_rect)

        #High Score
        if self.high_score > 0:
            high_score_text = game_font.render(f"High Score: {self.high_score}", True, golden_yellow)
            high_score_rect = high_score_text.get_rect(center=(window_width // 2, window_height // 2 - 20))
            game_window.blit(high_score_text, high_score_rect)

        #Start instruction
        start_text = game_font.render("Press SPACE or ENTER to Start", True, white)
        start_rect = start_text.get_rect(center=(window_width // 2, window_height // 2 + 30))
        game_window.blit(start_text, start_rect)

        #Controls header
        controls_header = game_font.render("- Controls -", True, cream)
        controls_header_rect = controls_header.get_rect(center=(window_width // 2, window_height // 2 + 80))
        game_window.blit(controls_header, controls_header_rect)

        #Controls
        controls = [
            "Arrow Keys or WASD - Move",
            "P - Pause Game",
            "ESC - Quit Game"
        ]
        
        for i, control in enumerate(controls):
            control_text = small_font.render(control, True, cream)
            control_rect = control_text.get_rect(center=(window_width // 2, window_height // 2 + 115 + i * 25))
            game_window.blit(control_text, control_rect)

        #Quit instruction
        quit_text = small_font.render("Press ESC to Quit", True, red)
        quit_rect = quit_text.get_rect(center=(window_width // 2, window_height - 30))
        game_window.blit(quit_text, quit_rect)

    def draw_paused(self):
        #Draw pause screen overlay
        window_width = screen_width * cell_size
        window_height = screen_height * cell_size
        
        #Semi-transparent overlay
        overlay = pygame.Surface((window_width, window_height))
        overlay.set_alpha(180)
        overlay.fill(black)
        game_window.blit(overlay, (0, 0))

        #Paused text
        pause_text = big_font.render("PAUSED", True, golden_yellow)
        text_rect = pause_text.get_rect(center=(window_width // 2, window_height // 2 - 40))
        game_window.blit(pause_text, text_rect)

        #Resume instruction
        resume_text = game_font.render("Press P to Resume", True, white)
        resume_rect = resume_text.get_rect(center=(window_width // 2, window_height // 2 + 10))
        game_window.blit(resume_text, resume_rect)

        #Menu instruction
        menu_text = game_font.render("Press M for Main Menu", True, white)
        menu_rect = menu_text.get_rect(center=(window_width // 2, window_height // 2 + 45))
        game_window.blit(menu_text, menu_rect)

        #Quit instruction
        quit_text = game_font.render("Press ESC to Quit", True, red)
        quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 80))
        game_window.blit(quit_text, quit_rect)

    def draw_game_over(self):
        #Draw game over screen#
        window_width = screen_width * cell_size
        window_height = screen_height * cell_size
        
        #Semi-transparent overlay
        overlay = pygame.Surface((window_width, window_height))
        overlay.set_alpha(180)
        overlay.fill(black)
        game_window.blit(overlay, (0, 0))

        #Game Over text
        game_over_text = big_font.render("GAME OVER!", True, red)
        text_rect = game_over_text.get_rect(center=(window_width // 2, window_height // 2 - 80))
        game_window.blit(game_over_text, text_rect)

        #Final score
        score = (len(self.caterpillar.body) - 3) * 10
        score_text = game_font.render(f"Final Score: {score}", True, golden_yellow)
        score_rect = score_text.get_rect(center=(window_width // 2, window_height // 2 - 40))
        game_window.blit(score_text, score_rect)

        #High score
        if score >= self.high_score and score > 0:
            new_high_text = game_font.render("NEW HIGH SCORE!", True, green)
            new_high_rect = new_high_text.get_rect(center=(window_width // 2, window_height // 2 - 10))
            game_window.blit(new_high_text, new_high_rect)
        else:
            high_score_text = game_font.render(f"High Score: {self.high_score}", True, cream)
            high_score_rect = high_score_text.get_rect(center=(window_width // 2, window_height // 2 - 10))
            game_window.blit(high_score_text, high_score_rect)

        #Food eaten
        food_eaten = len(self.caterpillar.body) - 3
        food_text = game_font.render(f"Food Eaten: {food_eaten}", True, green)
        food_rect = food_text.get_rect(center=(window_width // 2, window_height // 2 + 25))
        game_window.blit(food_text, food_rect)

        #Restart instruction
        restart_text = game_font.render("Press SPACE to Restart", True, white)
        restart_rect = restart_text.get_rect(center=(window_width // 2, window_height // 2 + 70))
        game_window.blit(restart_text, restart_rect)

        #Menu instruction
        menu_text = game_font.render("Press M for Main Menu", True, white)
        menu_rect = menu_text.get_rect(center=(window_width // 2, window_height // 2 + 105))
        game_window.blit(menu_text, menu_rect)

        #Quit instruction
        quit_text = game_font.render("Press ESC to Quit", True, red)
        quit_rect = quit_text.get_rect(center=(window_width // 2, window_height // 2 + 140))
        game_window.blit(quit_text, quit_rect)

    def draw_background(self):
        for row in range(1, screen_height):
            for col in range(screen_width):
                if (row + col) % 2 == 0:
                    rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(game_window, dark_brown, rect)

    def draw_score(self):
        score = (len(self.caterpillar.body) - 3) * 10
        food = len(self.caterpillar.body) - 3
        length = len(self.caterpillar.body)

        board = pygame.Rect(0, 0, screen_width * cell_size, cell_size)
        pygame.draw.rect(game_window, black, board)

        s1 = game_font.render(f"Score: {score}", True, golden_yellow)
        s2 = game_font.render(f"Food: {food}", True, green)
        s3 = game_font.render(f"Length: {length}", True, cream)

        game_window.blit(s1, s1.get_rect(left=10, centery=board.centery))
        game_window.blit(s2, s2.get_rect(center=board.center))
        game_window.blit(s3, s3.get_rect(right=board.right - 10, centery=board.centery))


#RUN
main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            # menu
            if main_game.state == state_menu:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                    main_game.start_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # playing
            elif main_game.state == state_playing:
                if event.key in (pygame.K_UP, pygame.K_w) and main_game.caterpillar.direction.y != 1:
                    main_game.caterpillar.direction = Vector2(0, -1)
                elif event.key in (pygame.K_DOWN, pygame.K_s) and main_game.caterpillar.direction.y != -1:
                    main_game.caterpillar.direction = Vector2(0, 1)
                elif event.key in (pygame.K_LEFT, pygame.K_a) and main_game.caterpillar.direction.x != 1:
                    main_game.caterpillar.direction = Vector2(-1, 0)
                elif event.key in (pygame.K_RIGHT, pygame.K_d) and main_game.caterpillar.direction.x != -1:
                    main_game.caterpillar.direction = Vector2(1, 0)
                elif event.key == pygame.K_p:
                    main_game.toggle_pause()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # paused
            elif main_game.state == state_paused:
                if event.key == pygame.K_p:
                    main_game.toggle_pause()
                elif event.key == pygame.K_m:
                    main_game.go_to_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # game over
            elif main_game.state == state_game_over:
                if event.key == pygame.K_SPACE:
                    main_game.reset_game()
                elif event.key == pygame.K_m:
                    main_game.go_to_menu()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    game_window.fill(light_brown)
    main_game.draw()
    pygame.display.update()
    clock.tick(fps)