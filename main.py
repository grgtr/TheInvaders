import pygame as pg
import sys
import os

from field import *
from unit import *

field_size = 10, 10
hex_size = 60, 70  # Размер гексов (6:7)
screen_size = width, height = field_size[0] * hex_size[0], field_size[1] * hex_size[1]  # Размер экрана


def main():
    pg.init()
    screen = pg.display.set_mode(screen_size)
    is_run = True

    # Загрузка данных
    field = Field(screen_size, field_size)
    field.generate()
    unit = Unit(100, 0, 15, 2, 5, 30, 35)
    while is_run:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if mouse_x - unit.x <= hex_size[0]:
                    pass
                print(mouse_x, mouse_y)

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
