import pygame as pg
import sys
import os

from classes import *

screen_size = width, height = 1000, 800
field_size = 15, 12


def main():
    pg.init()
    screen = pg.display.set_mode(screen_size)
    is_run = True

    # Загрузка данных
    field = Field(screen_size, field_size)

    while is_run:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.QUIT:
                is_run = False

        # Логика работы

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        field.draw(screen)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
