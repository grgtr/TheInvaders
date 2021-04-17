import pygame as pg
import sys
import os
import math

from field import *
from unit import *

field_size = 25, 14
hex_size = 60, 70  # Размер гексов (6:7)
screen_size = width, height = field_size[0] * hex_size[0], field_size[1] * hex_size[1]  # Размер экрана
colors = {
    'White': (255, 255, 255),
    'Black': (0, 0, 0),
    'DarkGoldenRod': (184, 134, 11),
    'Tan': (210, 180, 140),
    'SaddleBrown': (139, 69, 19),
}


# Отрисовка панели управления
def panel_draw(size: (int, int)):
    panel = pg.Surface(size)
    panel.fill(colors['SaddleBrown'])  # Заливка фона
    panel.blit(button_draw((size[1], size[1]), 'next'), (size[0] - size[1], 0))  # Кнопка следующего хода
    # Кнопка защиты
    # Кнопка торговли
    return panel


# Отрисовка кнопки
def button_draw(size: (int, int), form: str):
    btn = pg.Surface(size)  # Поверхность кнопки
    btn.fill(colors['SaddleBrown'])  # Фоновый цвет
    pg.draw.circle(btn, colors['DarkGoldenRod'], (size[1] // 2, size[1] // 2), size[1] // 2)  # Круг
    if form == 'next':
        pg.draw.polygon(btn, colors['Tan'], [  # Треугольник
            [size[1] // 3, size[1] // 4],
            [size[1] // 3, size[1] // 4 * 3],
            [size[1] // 4 * 3, size[1] // 2],
        ])
    elif form == 'attack':
        # img = pg.image.load(path)  # Загрузка картинки
        # img = pg.transform.scale(img, size)  # Масштабирование
        # screen.blit(img, img.get_rect(bottomright=(w, h)))  # Отрисовка
        pass
    elif form == 'defense':
        pass
    return btn


def main():
    pg.init()
    screen = pg.display.set_mode((screen_size[0], screen_size[1]))
    is_run = True

    # Загрузка данных
    field = Field(screen_size, field_size)
    # field.generate()
    field.gen_given_field()
    unit = Unit(100, 0, 15, 2, 5, int(hex_size[0] / 2), int(hex_size[1] / 2))
    while is_run:
        # Обработка событий
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pg.QUIT:
                is_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                l = int(math.sqrt(
                    (mouse_x - unit.x) ** 2 + (mouse_y - unit.y) ** 2))  # длина от центра юнита до нажатого гекса
                if int(hex_size[1] / 2) < l < int(hex_size[1]):  # длина  соответсвует соседнему гексу из 6
                    if (mouse_x > unit.x) and (
                            -int(hex_size[1] / 2) < mouse_y - unit.y < int(hex_size[1] / 2)):  # вправо
                        unit.x += int(hex_size[0])
                    elif (mouse_x < unit.x) and (
                            -int(hex_size[1] / 2) < mouse_y - unit.y < int(hex_size[1] / 2)):  # влево
                        unit.x -= int(hex_size[0])
                    elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y > unit.y):  # вправо вниз
                        unit.y += int(hex_size[1] - hex_size[1] / 4)
                        unit.x += int(hex_size[0] / 2)
                    elif (0 < unit.x - mouse_x < int(hex_size[0] / 2)) and (mouse_y > unit.y):  # влево вниз
                        unit.y += int(hex_size[1] - hex_size[1] / 4)
                        unit.x -= int(hex_size[0] / 2)
                    elif (0 < unit.x - mouse_x < int(hex_size[0] / 2)) and (mouse_y < unit.y):  # влево вверх
                        unit.y -= int(hex_size[1] - hex_size[1] / 4)
                        unit.x -= int(hex_size[0] / 2)
                    elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y < unit.y):  # вправо вверх
                        unit.y -= int(hex_size[1] - hex_size[1] / 4)
                        unit.x += int(hex_size[0] / 2)

        # Логика работы

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        field.draw(screen)
        unit.draw(screen)
        panel_size = (screen_size[0], 230)  # Размер панели управления
        panel_coord = (0, 750)  # Координаты панели управления
        screen.blit(panel_draw(panel_size), panel_coord)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
