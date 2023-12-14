import pygame
import random
from pygame.math import Vector2

cell_number = 20
cell_size = 40
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
apple = pygame.image.load('src/Images/apple.png').convert_alpha()

class Snake:
    def __init__(self):
        pygame.mixer.music.load('src/Sounds/foo.mp3') #ну а зачем целый класс для музыки с двумя строчками
        pygame.mixer.music.play(-1) #пусть на фоне
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]  #да, можно ввести две переменные,
        #зарандомить и относительно них рисовать змею (не вижу смысла)
        self.direction = Vector2(1, 0) #чтобы сразу поползла
        self.new_block = False

        self.head_up = pygame.image.load('src/Images/head_up_gr.png').convert_alpha()
        self.head_down = pygame.image.load('src/Images/head_down_gr.png').convert_alpha()
        self.head_right = pygame.image.load('src/Images/head_right_gr.png').convert_alpha()
        self.head_left = pygame.image.load('src/Images/head_left_gr.png').convert_alpha()

        self.tail_up = pygame.image.load('src/Images/tail_up_gr.png').convert_alpha()
        self.tail_down = pygame.image.load('src/Images/tail_down_gr.png').convert_alpha()
        self.tail_right = pygame.image.load('src/Images/tail_right_gr.png').convert_alpha()
        self.tail_left = pygame.image.load('src/Images/tail_left_gr.png').convert_alpha()

        self.body_vertical = pygame.image.load('src/Images/body_vertical_gr.png').convert_alpha()
        self.body_horizontal = pygame.image.load('src/Images/body_horizontal_gr.png').convert_alpha()

        self.body_tr = pygame.image.load('src/Images/body_tr_gr.png').convert_alpha()
        self.body_tl = pygame.image.load('src/Images/body_tl_gr.png').convert_alpha()
        self.body_br = pygame.image.load('src/Images/body_br_gr.png').convert_alpha()
        self.body_bl = pygame.image.load('src/Images/body_bl_gr.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('src/Sounds/кусь.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * 40)
            y_pos = int(block.y * 40)
            block_rect = pygame.Rect(x_pos, y_pos, 40, 40)

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

    def play_loser_sound(self) -> object:
        pygame.mixer.music.load('src/Sounds/game-lost.wav')
        pygame.mixer.music.play(0)

    #!!!! вери импортант след функция
    def reset(self): #ну я не буду удалять функцию потому что на 174 пытаюсь её реализовать но не понимаю
        #что не так (она должна начинать игру снова при нажатии пробела в гейм овер
        #но почему триггерится только кнопка эскейп и куит
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0) #чтобы на месте стояла

class Fruit:
    def __init__(self):
        self.x = None
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


