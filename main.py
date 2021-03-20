import pygame as pg
import sys
import os
import math

from field import *
from unit import *

field_size = 25, 15
hex_size = 60, 70  # Размер гексов (6:7)
screen_size = width, height = field_size[0] * hex_size[0], field_size[1] * hex_size[1]  # Размер экрана



def main():
    pg.init()
    screen = pg.display.set_mode(screen_size)
    is_run = True

    # Загрузка данных
    field = Field(screen_size, field_size)
    #field.generate()
    field.gen_given_field()
    print(field.field)
    unit = Unit(100, 0, 15, 2, 5, int(hex_size[0]/2), int(hex_size[1]/2))
    while is_run:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                print(mouse_x, mouse_y)
            if event.type == pg.QUIT:
                is_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                l = int(math.sqrt((mouse_x - unit.x) ** 2 + (mouse_y - unit.y) ** 2)) # длина от центра юнита до нажатого гекса
                if int(hex_size[1]/2) < l < int(hex_size[1]): # длина  соответсвует соседнему гексу из 6
                    if (mouse_x > unit.x) and (-int(hex_size[1]/2) < mouse_y - unit.y < int(hex_size[1]/2)): # вправо
                        unit.x += int(hex_size[0])
                    elif (mouse_x < unit.x) and (-int(hex_size[1]/2) < mouse_y - unit.y < int(hex_size[1]/2)):# влево
                        unit.x -= int(hex_size[0])
                    elif (0 < mouse_x - unit.x < int(hex_size[0]/2)) and (mouse_y > unit.y):# вправо вниз
                        unit.y += int(hex_size[1]-hex_size[1]/4)
                        unit.x += int(hex_size[0]/2)
                    elif (0 <unit.x - mouse_x < int(hex_size[0]/2)) and (mouse_y > unit.y): # влево вниз
                        unit.y += int(hex_size[1]-hex_size[1]/4)
                        unit.x -= int(hex_size[0]/2)
                    elif (0 < unit.x - mouse_x < int(hex_size[0]/2)) and (mouse_y < unit.y): # влево вверх
                        unit.y -= int(hex_size[1]-hex_size[1]/4)
                        unit.x -= int(hex_size[0]/2)
                    elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y < unit.y):# вправо вверх
                        unit.y -= int(hex_size[1] - hex_size[1] / 4)
                        unit.x += int(hex_size[0] / 2)




        # Логика работы

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        field.draw(screen)
        unit.draw(screen)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
