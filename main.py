import pygame as pg
import sys
import os
import math
from math import ceil
from field import *
from unit import *
from player import *

field_size = 25, 14
hex_size = 60, 70  # Размер гексов (6:7)
screen_size = width, height = field_size[0] * hex_size[0], field_size[1] * hex_size[1]  # Размер экрана
colors = {
    'White': (255, 255, 255),
    'Black': (0, 0, 0),
    'DarkGoldenRod': (184, 134, 11),
    'Tan': (210, 180, 140),
    'SaddleBrown': (139, 69, 19),
    'светло жёлтый': (255, 217, 73)
}
move_counter = 0  # Счетчик ходов
panel_size = (screen_size[0], 230)  # Размер панели управления

def point_in(x,y):
    ans = False
    hx = 0
    hy = 0
    for hx in range(0,field_size[0]):
        if not ans:
            for hy in range(0,field_size[1]):
                if not ans:
                    if hy % 2 == 0:
                        if (x < (hx + 1)*hex_size[0]) and (x > hx*hex_size[0]) and (y > int(ceil(-2/3 * x + 2/7 * hex_size[1] * (2*hx+1) + 10/7 * hex_size[1] * (y//2)))) and (y < int(ceil(-2/3 * x + 2/7 * hex_size[1] * (2*hx+1) + 10/7 * hex_size[1] * (y//2) + hex_size[1]))) and (y > int(ceil(2/3 * x + 2/7 * hex_size[1] * (2*hx-1) + 10/7 * hex_size[1] * (y//2)))) and (y < int(ceil(2/3 * x + 2/7 * hex_size[1] * (2*hx-1) + 10/7 * hex_size[1] * (y//2)))):
                            return hx, hy
                        ans = True
                    elif hy % 2 == 1:
                        if (x > hx *hex_size[0] + hex_size[0] // 2) and (x < hx *hex_size[0] + 3 * hex_size[0] // 2) and (y < int(ceil(-2/3 * x + 2/7 * hex_size[1] * (2*hx+1) + 10/7 * hex_size[1] * ((y-1)//2)))) and (y > int(ceil(-2/3 * x + 2/7 * hex_size[1] * (2*hx+1) + 10/7 * hex_size[1] * (y//2) + hex_size[1]))) and (y < int(ceil(2/3 * x + 2/7 * hex_size[1] * (2*hx-1) + 10/7 * hex_size[1] * (y//2)))) and (y > int(ceil(2/3 * x + 2/7 * hex_size[1] * (2*hx-1) + 10/7 * hex_size[1] * (y//2)))):
                            return hx, hy
                        ans = True

# Отрисовка панели управления
def panel_draw(size: (int, int), screen):
    panel = pg.Surface(size)
    panel.fill(colors['SaddleBrown'])  # Заливка фона
    panel.blit(button_draw((size[1], size[1]), 'next', screen), (size[0] - size[1], 0))  # Кнопка следующего хода
    panel.blit(button_draw((size[1], size[1]), 'attack', screen), (size[0] - 2 * size[1], 0))  # Кнопка атаки
    panel.blit(button_draw((size[1], size[1]), 'trade', screen), (size[0] - 3 * size[1], 0))  # Кнопка защиты
    panel.blit(button_draw((size[1], size[1]), 'select', screen), (size[0] - 4 * size[1], 0))  # Кнопка след юнит
    '''panel.blit(button_draw((size[1], size[1]), 'trade'), (size[0] - 4*size[1], 0))  # Кнопка торговли
    panel.blit(button_draw((size[1], size[1]), 'select'), (size[0] - 5*size[1], 0))  # Кнопка торговли'''
    return panel


# Отрисовка кнопки
def button_draw(size: (int, int), form: str, screen):
    btn = pg.Surface(size)  # Поверхность кнопки
    btn.fill(colors['SaddleBrown'])  # Фоновый цвет
    pg.draw.circle(btn, colors['DarkGoldenRod'], (size[1] // 2, size[1] // 2), size[1] // 2)  # Круг
    if form == 'next':
        pg.draw.polygon(btn, colors['светло жёлтый'], [  # Треугольник
            [size[1] // 3, size[1] // 4],
            [size[1] // 3, size[1] // 4 * 3],
            [size[1] // 4 * 3, size[1] // 2],
        ])
        btn.blit(pg.font.Font(None, 20).render(f'Ход {move_counter}', True, colors['Black']),  # Отрисовка счетчика хода
                 (size[0] // 2 - 25, size[1] - 40))
    elif form == 'attack':
        img = pg.image.load('buttons/attack.png')  # Загрузка картинки
        img = pg.transform.scale(img, (int(size[1] / 1.4), int(size[1] / 1.5)))  # Масштабирование
        btn.blit(img, img.get_rect(bottomright=(size[1] // 1.2, size[1] // 1.2)))  # Отрисовка
    elif form == 'defense':
        '''
        img = pg.image.load('buttons/defend.png')  # Загрузка картинки
        img = pg.transform.scale(img, (int(size[1] / 1.3), int(size[1] / 1.3)))  # Масштабирование
        btn.blit(img, img.get_rect(bottomright=(4.4 * size[1], int(3.6 * size[1]))))  # Отрисовка
        '''
        pass
    elif form == 'trade':
        img = pg.image.load('buttons/trade.png')  # Загрузка картинки
        img = pg.transform.scale(img, (int(size[1] / 1.1), int(size[1] / 1.1)))  # Масштабирование
        btn.blit(img, img.get_rect(bottomright=(0.95 * size[1], int(1.0 * size[1]))))  # Отрисовка
    elif form == 'select':
        """img = pg.image.load(path)  # Загрузка картинки
        img = pg.transform.scale(img, size)  # Масштабирование
        screen.blit(img, img.get_rect(bottomright=(w, h)))  # Отрисовка"""
        pass
    return btn


def main():
    pg.init()
    screen = pg.display.set_mode((screen_size[0], screen_size[1]))
    is_run = True
    a = []
    player1 = Player(100, a)
    player1.add_unit(Unit(100, 0, 15, 0, 2, 10, int(3*hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size))
    a = []
    player2 = Player(100, a)
    player2.add_unit(Unit(100, 0, 15, 0, 2, 10, int(24*hex_size[0]- hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size))
    # Загрузка данных
    field = Field(screen_size, field_size)
    # field.generate()
    field.gen_given_field()
    #unit = Unit(100, 0, 15, 0, 2, 5, int(3*hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size)
    button_select_pressed = False
    now = 0
    while is_run:
        # Обработка событий
        global move_counter
        if move_counter % 2 == 0:
            unit = player1.units[now]
        else:
            unit = player2.units[now]
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                print(mouse_x, mouse_y)
            if event.type == pg.QUIT:
                is_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                print(point_in(mouse_x, mouse_y))
                # Нажатие на кнопку следующего хода
                if (panel_size[0] - panel_size[1] < mouse_x) and (screen_size[1] - panel_size[1] < mouse_y):
                    move_counter += 1
                    now = 0
                # Нажатие на кнопку следующего trade
                if (mouse_x - 925) ** 2 + (mouse_y - 865) ** 2 < 115 ** 2:
                    if (unit.y - 35) % 100 == 0:
                        uhy = ((unit.y-35) // 100)
                        uhy += uhy
                        uhx = ((unit.x - 30) // 60)
                    else:
                        uhy = ((unit.y-85) // 100)
                        uhy += uhy + 1
                        uhx = ((unit.x - 1) // 60)
                    # print('unit', unit.x, unit.y)
                    # print('hex ', uhx, uhy)
                    print(field.field[uhy][uhx][0])
                    if field.field[uhy][uhx][0] == 'medieval':
                        if move_counter % 2 == 0:
                            player1.add_unit(Unit(100, 0, 15, 0, 2, 10, int(3*hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size))
                        else:
                            player2.add_unit(Unit(100, 0, 15, 0, 2, 10, int(24*hex_size[0]- hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size))

                # Нажатие на кнопку следующего unit
                if (mouse_x - 695)**2 + (mouse_y-865)**2 < 115**2:
                    if move_counter % 2 == 0:
                        if now + 1 == len(player1.units):
                            now = 0
                        else:
                            now += 1
                        unit = player1.units[now]
                        print('now', now, len(player1.units))
                    else:
                        if now + 1 == len(player2.units):
                            now = 0
                        else:
                            now += 1
                        unit = player2.units[now]
                        print('now', now, len(player2.units))



                l = int(math.sqrt(
                    (mouse_x - unit.x) ** 2 + (mouse_y - unit.y) ** 2))  # длина от центра юнита до нажатого гекса
                if int(hex_size[1] / 2) < l < int(hex_size[1]):  # длина соответствует соседнему гексу из 6
                    if (mouse_x > unit.x) and (
                            -int(hex_size[1] / 2) < mouse_y - unit.y < int(hex_size[1] / 2)):  # вправо
                        unit.x += int(hex_size[0])
                    elif (mouse_x < unit.x) and (
                            -int(hex_size[1] / 2) < mouse_y - unit.y < int(hex_size[1] / 2)):  # влево
                        unit.x -= int(hex_size[0])
                    elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y > unit.y):  # вправо вниз
                        unit.y += int(ceil(5/7*hex_size[1]))
                        unit.x += int(hex_size[0] / 2)
                    elif (0 < unit.x - mouse_x < int(hex_size[0] / 2)) and (mouse_y > unit.y):  # влево вниз
                        unit.y += int(ceil(5/7*hex_size[1]))
                        unit.x -= int(hex_size[0] / 2)
                    elif (0 < unit.x - mouse_x < int(hex_size[0] / 2)) and (mouse_y < unit.y):  # влево вверх
                        unit.y -= int(ceil(5/7*hex_size[1]))
                        unit.x -= int(hex_size[0] / 2)
                    elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y < unit.y):  # вправо вверх
                        unit.y -= int(ceil(5/7*hex_size[1]))
                        unit.x += int(hex_size[0] / 2)
                    print('unit', unit.x, unit.y)

        # Логика работы

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        field.draw(screen)
        #unit.draw(screen)
        for i in range(len(player1.units)):  # отображение юнитов игрока 1
            player1.units[i].draw(screen)

        for i in range(len(player2.units)):  # отображение юнитов игрока 2
            player2.units[i].draw(screen)

        panel_coord = (0, 750)  # Координаты панели управления
        screen.blit(panel_draw(panel_size, screen), panel_coord)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
