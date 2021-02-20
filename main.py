import pygame as pg
import sys
import os

from classes import *

field_size = 20, 10
screen_size = width, height = field_size[0] * 60, field_size[1] * 70  # Отношение размера экрана как и размер гексов 6:7


def main():
    pg.init()
    screen = pg.display.set_mode(screen_size)
    is_run = True

    # Загрузка данных
    field = Field(screen_size, field_size)
    field.generate()

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
