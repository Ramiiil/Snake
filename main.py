import pygame  # ну библии
import random
import sys
from pygame.math import Vector2  # для определения местоположения змейки


class SNAKE: #рисуем змею и выполняем с ней действия
    def __init__(self):
        pygame.mixer.music.load('Sound/foo.mp3') #ну а зачем целый класс для музыки с двумя строчками
        pygame.mixer.music.play(-1) #пусть на фоне
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  #да, можно ввести две переменные,
        #зарандомить и относительно них рисовать змею (не вижу смысла)
        self.direction = Vector2(1, 0) #чтобы сразу поползла
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up_gr.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down_gr.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right_gr.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left_gr.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up_gr.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down_gr.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right_gr.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left_gr.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical_gr.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal_gr.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr_gr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl_gr.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br_gr.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl_gr.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/кусь.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

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
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def play_loser_sound(self):
        pygame.mixer.music.load('Sound/game-lost.wav')
        pygame.mixer.music.play(0)

    #!!!! вери импортант след функция
    def reset(self): #ну я не буду удалять функцию потому что на 174 пытаюсь её реализовать но не понимаю
        #что не так (она должна начинать игру снова при нажатии пробела в гейм овер
        #но почему триггерится только кнопка эскейп и куит
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0) #чтобы на месте стояла

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.snake.play_loser_sound()
            while True:
                self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.snake.play_loser_sound()
                while True:
                    self.game_over()

    def game_over(self):
        render_end = game_over_font.render('GAME OVER', 1, pygame.Color('black'))
        screen.blit(render_end, (cell_number * cell_size - 550, cell_number * cell_size - 450))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_SPACE:
                    self.snake.reset()

    def draw_grass(self):
        grass_color = (209, 188, 138)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 750)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)
        pygame.draw.rect(screen, (209, 188, 138), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (244, 255, 0), bg_rect, 2)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
pygame.display.set_caption('Питончик смыкается')
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/Country Western Swing Title.ttf', 30)
game_over_font = pygame.font.Font('Font/A.D. MONO.ttf', 70)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w: #не всегда работает управление wasd (необьяснимо)
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((233, 229, 206))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(120)
