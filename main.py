import pygame as pg
import sys
import os
import math
from math import ceil
from field import *
from unit import *
from building import *
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
    'светло жёлтый': (255, 217, 73),
    'MediumSpringGreen': (0, 250, 154),
    'Yellow': (255, 255, 0),
}
move_counter = 0  # Счетчик ходов
panel_size = (screen_size[0], 230)  # Размер панели управления


def point_in(unit_x, unit_y):
    # print('pox, poy', unit_x, unit_y)
    if (unit_y - 35) % 105 == 0:
        # print('chet')
        uhy = ((unit_y - 35) // 105)
        uhy += uhy
        uhx = ((unit_x - 30) // 60)
    else:
        # print('nechet')
        uhy = ((unit_y - 85) // 105)
        uhy += uhy + 1
        uhx = ((unit_x - 1) // 60)
    return uhx, uhy


def center_hex(uhx, uhy):
    x = 0
    y = 0
    if uhy % 2 == 0:
        x = 30 + 60 * uhx
        y = 35 + (uhy // 2) * 105
    else:
        x = 60 + 60 * uhx
        y = 85 + (((uhy + 1) // 2) - 1) * 105
    return x, y


def who_on(hx, hy, units):
    for i in range(len(units)):
        uhx, uhy = point_in(units[i].x, units[i].y)
        if hx == uhx and hy == uhy:
            return units[i]


def any_on(hx, hy, units):
    for i in range(len(units)):
        uhx, uhy = point_in(units[i].x, units[i].y)
        if hx == uhx and hy == uhy:
            return True
    return False


def mouse_in(mx, my):
    # print('pox, poy', unit_x, unit_y)
    hy1 = (my - 35) // 100
    hy1 += hy1
    hx1 = (mx - 30) // 60
    hy2 = (my - 85) // 105
    hy2 += hy2 + 1
    hx2 = (mx - 1) // 60
    centres1 = [(hx1 - 1, hy1 - 1), (hx1, hy1 - 1), (hx1 + 1, hy1), (hx1, hy1 + 1), (hx1 - 1, hy1 + 1),
                (hx1 - 1, hy1)]
    centres2 = [(hx2, hy2 - 1), (hx2 + 1, hy2 - 1), (hx2 + 1, hy2), (hx2 + 1, hy2 + 1), (hx2, hy2 + 1),
                (hx2 - 1, hy2)]
    stop = True
    li = 0
    while stop:
        if li == 6:
            stop = False
            li = 0
        # print('li =', li)
        uhxl, uhyl = centres1[li]
        # print('uhxl, uhyl', uhxl, uhyl)
        x, y = center_hex(uhxl, uhyl)
        # print('center', x , y)
        # print('mouse', mouse_x, mouse_y)
        if (mx - x) ** 2 + (my - y) ** 2 < 30 ** 2:
            stop = False
            li = 0
            return uhxl, uhyl
        else:
            li += 1
    stop = True
    li = 0
    while stop:
        if li == 6:
            stop = False
            li = 0
        # print('li =', li)
        uhxl, uhyl = centres2[li]
        # print('uhxl, uhyl', uhxl, uhyl)
        x, y = center_hex(uhxl, uhyl)
        # print('center', x , y)
        # print('mouse', mouse_x, mouse_y)
        if (mx - x) ** 2 + (my - y) ** 2 < 30 ** 2:
            stop = False
            li = 0
            return uhxl, uhyl
        else:
            li += 1


# Отрисовка панели управления
def panel_draw(size: (int, int), screen, sel_unit: Unit, sel_player: Player):
    panel = pg.Surface(size)
    panel.fill(colors['SaddleBrown'])  # Заливка фона
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'next', screen),
               (size[0] - size[1] / 2, size[1] / 2))  # Кнопка следующего хода
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'attack', screen),
               (size[0] - size[1], size[1] / 2))  # Кнопка атаки
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'trade', screen), (size[0] - size[1] / 2, 0))  # Кнопка защиты
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'select', screen), (size[0] - size[1], 0))  # Кнопка след юнит
    '''panel.blit(button_draw((size[1], size[1]), 'trade'), (size[0] - 4*size[1], 0))  # Кнопка торговли
    panel.blit(button_draw((size[1], size[1]), 'select'), (size[0] - 5*size[1], 0))  # Кнопка торговли'''
    # Отрисовка характеристик выбранного юнита
    text = [f'Параметры выбранного юнита:',
            f'Здоровье: {sel_unit.hp}/{sel_unit.max_hp}',
            f'Сила атаки: {sel_unit.dmg}',
            f'Защита: {sel_unit.defense}',
            f'Уровень: {sel_unit.lvl + 1}',
            f'Опыт: {sel_unit.exp}',
            f'Очки перемещения: {sel_unit.moves}/{sel_unit.max_moves}',
            f'Мана: {sel_unit.mana}/{sel_unit.max_mana}',
            ]
    for i in range(len(text)):
        panel.blit(pg.font.Font(None, 25).render(text[i], True, colors['MediumSpringGreen']), (10, 10 + i * 25))
    # Информация об игроке
    panel.blit(pg.font.Font(None, 25).render(f'Игрок {move_counter % 2 + 1}', True, colors['MediumSpringGreen']),
               (size[0] / 2, size[1] / 2 - 25))
    panel.blit(pg.font.Font(None, 25).render(f'Монеты: {sel_player.money} квач', True, colors['MediumSpringGreen']),
               (size[0] / 2, size[1] / 2))
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
    b = []
    med_bld = ['Небольшая мельница.Приносит 5 золота в ход.', 'Изящная арка',
               'Кузница позволяет улучшать оружие и броню.', 'Таверна.Ускоренная регенирация +10 hp',
               'Старое Кладбище.Купите карту, чтобы найти сокровище', 'Ферма.Приносит 10 золота в ход',
               'Таверна наёмников.Можно нанять войска',
               'Замок наёмников. Можно нанять усовершенствованные войска.', 'Местная пекарня.Приносит 10 золота в ход',
               'Небольшой замок.Приносит 15 золота в ход',
               'Королевский замок.Приносит 15 золота в ход,можно нанимать войска',
               'Сокровище. 50 золота , +5 к силе оружия', 'Золотой рудник.Приносит 20 золота в ход',
               'Башня магов.Можно нанять магов за золото и очки знаменитости', 'Лагерь разбойников']
    player1 = Player(100, a, b)
    player1.add_unit(
        Unit(100, 0, 15, 0, 2, 10, int(3 * hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size))
    a = []
    b = []
    player2 = Player(100, a, b)
    player2.add_unit(
        Unit(100, 0, 15, 0, 2, 10, int(24 * hex_size[0] - hex_size[0] / 2), int(hex_size[1] / 2), screen_size,
             field_size))
    # Загрузка данных
    field = Field(screen_size, field_size)
    # field.generate()
    field.gen_given_field()
    # unit = Unit(100, 0, 15, 0, 2, 5, int(3*hex_size[0] / 2), int(hex_size[1] / 2), screen_size, field_size)
    button_select_pressed = False
    now = 0
    attack = False
    while is_run:
        # Обработка событий
        global move_counter
        if move_counter % 2 == 0:
            enemy = player2
            player = player1
            unit = player1.units[now]
        else:
            enemy = player1
            player = player2
            unit = player2.units[now]
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
                print(mouse_x, mouse_y)
            if event.type == pg.QUIT:
                is_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                try:
                    mhx, mhy = mouse_in(mouse_x, mouse_y)
                except:
                    break
                # print('mouse_in', mhx, mhy)
                uhx, uhy = point_in(unit.x, unit.y)
                # print('point_in unit', uhx, uhy)
                if attack:
                    if uhy % 2 == 0:
                        centres = [(uhx - 1, uhy - 1), (uhx, uhy - 1), (uhx + 1, uhy), (uhx, uhy + 1),
                                   (uhx - 1, uhy + 1),
                                   (uhx - 1, uhy)]
                    else:
                        centres = [(uhx, uhy - 1), (uhx + 1, uhy - 1), (uhx + 1, uhy), (uhx + 1, uhy + 1),
                                   (uhx, uhy + 1),
                                   (uhx - 1, uhy)]
                    # print(uhx, uhy, mhx, mhy)
                    if any_on(mhx, mhy, enemy.units):
                        attacker = who_on(uhx, uhy, player.units)
                        enemy_unit = who_on(mhx, mhy, enemy.units)
                        attacker.attack(enemy_unit)
                        attack = False
                    else:
                        attack = False
                elif not attack:
                    # Нажатие на кнопку следующего хода
                    if (mouse_x - 1445) ** 2 + (mouse_y - 922) ** 2 < 57 ** 2:
                        move_counter += 1
                        now = 0
                        player.refresh()
                        for i in range(len(player1.units)):  # отображение юнитов игрока 1
                            player1.units[i].refresh()

                        for i in range(len(player2.units)):  # отображение юнитов игрока 2
                            player2.units[i].refresh()
                    # Нажатие на кнопку следующего trade
                    elif (mouse_x - 1445) ** 2 + (mouse_y - 817) ** 2 < 57 ** 2:
                        if unit.moves > 0:

                            # print('+++')
                            # print('unit', unit.x, unit.y)
                            # print('hex ', uhx, uhy)
                            # print(field.field[uhy][uhx][0])
                            if field.field[uhy][uhx][0] == 'medieval':

                                # unit.moves -= 1
                                # x, y = center_hex(uhx, uhy)
                                # player.add_unit(
                                #     Unit(100, 0, 15, 0, 2, 10, x, y, screen_size,
                                #          field_size))
                                if field.field[uhy][uhx][1] == 0:
                                    pass
                                elif field.field[uhy][uhx][1] == 1:
                                    pass
                                elif field.field[uhy][uhx][1] == 2:
                                    if player.money >= 20:
                                        if player.step_forge + 2  <= move_counter:
                                            unit.moves = 0
                                            unit.dmg += 5
                                            player.money -= 20
                                            player.step_forge = move_counter
                                elif field.field[uhy][uhx][1] == 3:
                                    if player.money >= 10:
                                        if player.chet_step + 1 <= move_counter:
                                            unit.moves -= 1
                                            player.money -= 10
                                            player.chet_step = move_counter
                                            if player.treasure_map == 0:
                                                # TODO say u find a map!!!!!!!!!!!!!!!!!!!!!!
                                                player.treasure_map = 1
                                elif field.field[uhy][uhx][1] == 4:
                                        if player.treasure_map == 1:
                                            player.money += 50
                                            player.treasure_map = -1

                                elif field.field[uhy][uhx][1] == 5:
                                    pass
                                elif field.field[uhy][uhx][1] == 6:
                                    if player.money >= 50:
                                        unit.moves -= 1
                                        x, y = center_hex(uhx, uhy)
                                        player.add_unit(
                                            Unit(100, 0, 15, 0, 2, 10, x, y, screen_size,
                                                 field_size))
                                        player.money -= 50
                                elif field.field[uhy][uhx][1] == 7:
                                    if player.money >= 50:
                                        unit.moves -= 1
                                        x, y = center_hex(uhx, uhy)
                                        player.add_unit(
                                            Unit(100, 0, 15, 0, 2, 10, x, y, screen_size,
                                                 field_size))
                                        player.money -= 50
                                elif field.field[uhy][uhx][1] == 8:
                                    pass
                                elif field.field[uhy][uhx][1] == 9:
                                    pass
                                elif field.field[uhy][uhx][1] == 10:
                                    pass
                                elif field.field[uhy][uhx][1] == 11:
                                    if player.big_treasure == 0:
                                        unit.moves = 0
                                        unit.dmg += 15
                                        player.money += 250
                                        player.big_treasure = -1
                                elif field.field[uhy][uhx][1] == 12:
                                    pass
                                elif field.field[uhy][uhx][1] == 13:
                                    if player.money >= 50:
                                        unit.moves -= 1
                                        x, y = center_hex(uhx, uhy)
                                        player.add_unit(
                                            Unit(100, 0, 15, 0, 2, 10, x, y, screen_size,
                                                 field_size))
                                        player.money -= 50
                                elif field.field[uhy][uhx][1] == 14:
                                    pass


                    # Нажатие на кнопку следующего unit
                    elif (mouse_x - 1330) ** 2 + (mouse_y - 817) ** 2 < 57 ** 2:
                        if move_counter % 2 == 0:
                            if now + 1 == len(player1.units):
                                now = 0
                            else:
                                now += 1
                            unit = player1.units[now]
                            # print('now', now, len(player1.units))
                        else:
                            if now + 1 == len(player2.units):
                                now = 0
                            else:
                                now += 1
                            unit = player2.units[now]
                            # print('now', now, len(player2.units))
                    # Нажатие на кнопку attack
                    elif (mouse_x - 1330) ** 2 + (mouse_y - 922) ** 2 < 57 ** 2:
                        if unit.moves > 0:
                            if not any_on(uhx, uhy, player.units):
                                attack = True
                            # print(attack)
                    else:
                        if unit.moves > 0:
                            # uhx, uhy = point_in(unit.x, unit.y)
                            # print('uhx, uhy', uhx, uhy)
                            # по часовой
                            if uhy % 2 == 0:
                                centres = [(uhx - 1, uhy - 1), (uhx, uhy - 1), (uhx + 1, uhy), (uhx, uhy + 1),
                                           (uhx - 1, uhy + 1),
                                           (uhx - 1, uhy)]
                            else:
                                centres = [(uhx, uhy - 1), (uhx + 1, uhy - 1), (uhx + 1, uhy), (uhx + 1, uhy + 1),
                                           (uhx, uhy + 1),
                                           (uhx - 1, uhy)]
                            # print(centres)
                            stop = True
                            li = 0
                            while stop:
                                if li == 6:
                                    stop = False
                                    li = 0
                                # print('li =', li)
                                uhxl, uhyl = centres[li]
                                # print('uhxl, uhyl', uhxl, uhyl)
                                x, y = center_hex(uhxl, uhyl)
                                # print('center', x , y)
                                # print('mouse', mouse_x, mouse_y)
                                if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 < 30 ** 2:
                                    stop = False
                                    li = 0
                                    if not any_on(uhxl, uhyl, player.units) and not any_on(uhxl, uhyl, enemy.units):
                                        unit.x = x
                                        unit.y = y
                                        unit.moves -= 1
                                        hex_x, hex_y = point_in(unit.x, unit.y)
                                        if field.field[hex_y][hex_x][0] == 'medieval':
                                            player.add_building(Building(hex_x, hex_y, field.field[uhy][uhx][1]))
                                            # print('added', len(player.buildings))


                                else:
                                    li += 1

                        # if (mouse_x - c)
                        # l = int(math.sqrt(
                        #     (mouse_x - unit.x) ** 2 + (mouse_y - unit.y) ** 2))  # длина от центра юнита до нажатого гекса
                        # if int(hex_size[1] / 2) < l < int(hex_size[1]):  # длина соответствует соседнему гексу из 6
                        #     if (mouse_x > unit.x) and (
                        #             -int(hex_size[1] / 2) < mouse_y - unit.y < int(hex_size[1] / 2)):  # вправо
                        #         unit.x += int(hex_size[0])
                        #     elif (mouse_x < unit.x) and (
                        #             -int(hex_size[1] / 2) < mouse_y - unit.y < int(hex_size[1] / 2)):  # влево
                        #         unit.x -= int(hex_size[0])
                        #     elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y > unit.y):  # вправо вниз
                        #         unit.y += int(ceil(5 / 7 * hex_size[1]))
                        #         unit.x += int(hex_size[0] / 2)
                        #     elif (0 < unit.x - mouse_x < int(hex_size[0] / 2)) and (mouse_y > unit.y):  # влево вниз
                        #         unit.y += int(ceil(5 / 7 * hex_size[1]))
                        #         unit.x -= int(hex_size[0] / 2)
                        #     elif (0 < unit.x - mouse_x < int(hex_size[0] / 2)) and (mouse_y < unit.y):  # влево вверх
                        #         unit.y -= int(ceil(5 / 7 * hex_size[1]))
                        #         unit.x -= int(hex_size[0] / 2)
                        #     elif (0 < mouse_x - unit.x < int(hex_size[0] / 2)) and (mouse_y < unit.y):  # вправо вверх
                        #         unit.y -= int(ceil(5 / 7 * hex_size[1]))
                        #         unit.x += int(hex_size[0] / 2)
                        #     print('unit', unit.x, unit.y)

            # Логика работы

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        field.draw(screen)
        # unit.draw(screen)
        for i in range(len(player1.units)):  # отображение юнитов игрока 1
            player1.units[i].draw(screen)

        for i in range(len(player2.units)):  # отображение юнитов игрока 2
            player2.units[i].draw(screen)

        # Отрисовка рамки выбранного юнита
        pg.draw.polygon(screen, colors['Yellow'], [
            (unit.x - hex_size[0] / 2, unit.y - hex_size[1] / 4),
            (unit.x, unit.y - hex_size[1] / 2),
            (unit.x + hex_size[0] / 2, unit.y - hex_size[1] / 4),
            (unit.x + hex_size[0] / 2, unit.y + hex_size[1] / 4),
            (unit.x, unit.y + hex_size[1] / 2),
            (unit.x - hex_size[0] / 2, unit.y + hex_size[1] / 4),
        ], 3)

        panel_coord = (0, 750)  # Координаты панели управления
        screen.blit(panel_draw(panel_size, screen, unit, player), panel_coord)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
