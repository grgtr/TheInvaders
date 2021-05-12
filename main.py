"""Главный модуль программы"""
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
screen_size = width, height = field_size[0] * hex_size[0],\
                              field_size[1] * hex_size[1]  # Размер экрана
field: Field
colors = {
    'White': (255, 255, 255),
    'Black': (0, 0, 0),
    'DarkGoldenRod': (184, 134, 11),
    'Tan': (210, 180, 140),
    'SaddleBrown': (139, 69, 19),
    'светло жёлтый': (255, 217, 73),
    'MediumSpringGreen': (0, 250, 154),
    'Yellow': (255, 255, 0),
    'Red': (255, 0, 0),
    'DeepSkyBlue': (0, 191, 255),
}
MOVE_COUNTER = 0  # Счетчик ходов
panel_size = (screen_size[0], 230)  # Размер панели управления


def point_in(unit_x, unit_y) -> tuple[int, int]:
    """Проверка на нахождение гекса по координатам"""
    if (unit_y - 35) % 105 == 0:
        uhy = ((unit_y - 35) // 105)
        uhy += uhy
        uhx = ((unit_x - 30) // 60)
    else:
        uhy = ((unit_y - 85) // 105)
        uhy += uhy + 1
        uhx = ((unit_x - 1) // 60)
    return uhx, uhy


def center_hex(uhx, uhy) -> tuple[int, int]:
    """Поиск центра гекса по его координатам"""
    if uhy % 2 == 0:
        coord_x = 30 + 60 * uhx
        coord_y = 35 + (uhy // 2) * 105
    else:
        coord_x = 60 + 60 * uhx
        coord_y = 85 + (((uhy + 1) // 2) - 1) * 105
    return coord_x, coord_y


def who_on(coord_x, coord_y, units) -> Unit:
    """
    Какой юнит расположен на клетке
    :param coord_x: координата х
    :param coord_y: координата н
    :param units: массив юнитов
    :return: юнит, находящийся на клетке
    """
    for i in units:
        uhx, uhy = point_in(i.coord_x, i.coord_y)
        if (coord_x == uhx) and (coord_y == uhy):
            return i
    raise Exception('No units on the field')


def any_on(coord_x, coord_y, units) -> bool:
    """Проверка расположения на клетке какого-либо юнита"""
    for i in units:
        uhx, uhy = point_in(i.coord_x, i.coord_y)
        if (coord_x == uhx) and (coord_y == uhy):
            return True
    return False

def how_much_on(hx, hy, units):
    count = 0
    for i in range(len(units)):
        uhx, uhy = point_in(units[i].x, units[i].y)
        if hx == uhx and hy == uhy:
            count += 1
    return count

def mouse_in(mouse_x, mouse_y) -> tuple[int, int]:
    """Поиск гекса по координатам мыши"""
    hy1 = (mouse_y - 35) // 100
    hy1 += hy1
    hx1 = (mouse_x - 30) // 60
    hy2 = (mouse_y - 85) // 105
    hy2 += hy2 + 1
    hx2 = (mouse_x - 1) // 60
    centres1 = [(hx1 - 1, hy1 - 1), (hx1, hy1 - 1), (hx1 + 1, hy1),
                (hx1, hy1 + 1), (hx1 - 1, hy1 + 1), (hx1 - 1, hy1)]
    centres2 = [(hx2, hy2 - 1), (hx2 + 1, hy2 - 1), (hx2 + 1, hy2),
                (hx2 + 1, hy2 + 1), (hx2, hy2 + 1), (hx2 - 1, hy2)]
    stop = True
    counter = 0
    while stop:
        if counter == 6:
            stop = False
            counter = 0
        unit_hex_x_edited, unit_hex_y_edited = centres1[counter]
        center_x, center_y = center_hex(unit_hex_x_edited, unit_hex_y_edited)
        if (mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2 < 30 ** 2:
            return unit_hex_x_edited, unit_hex_y_edited
        counter += 1
    stop = True
    counter = 0
    while stop:
        if counter == 6:
            stop = False
            counter = 0
        unit_hex_x_edited, unit_hex_y_edited = centres2[counter]
        center_x, center_y = center_hex(unit_hex_x_edited, unit_hex_y_edited)
        if (mouse_x - center_x) ** 2 + (mouse_y - center_y) ** 2 < 30 ** 2:
            return unit_hex_x_edited, unit_hex_y_edited
        counter += 1


def panel_draw(size: (int, int), sel_unit: Unit, sel_player: Player) -> pg.Surface:
    """
    Отрисовка панели управления
    :param size: размер панели управления
    :param sel_unit: выбранный юнит
    :param sel_player: текущий игрок
    :return: поверхность с отрисованной панелью
    """
    panel = pg.Surface(size)
    panel.fill(colors['SaddleBrown'])  # Заливка фона
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'next'),
               (size[0] - size[1] / 2, size[1] / 2))  # Кнопка следующего хода
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'attack'),
               (size[0] - size[1], size[1] / 2))  # Кнопка атаки
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'trade'),  # Кнопка торговли
               (size[0] - size[1] / 2, 0))
    panel.blit(button_draw((size[1] / 2, size[1] / 2), 'select'),  # Кнопка следующего юнита
               (size[0] - size[1], 0))
    # Информация о выбранном юните
    text = ['Параметры выбранного юнита:',
            f'{sel_unit.title}',
            f'Здоровье: {sel_unit.health}/{sel_unit.max_hp}',
            f'Сила атаки: {sel_unit.dmg}',
            f'Защита: {sel_unit.defense}',
            f'Уровень: {sel_unit.lvl + 1}',
            f'Опыт: {sel_unit.exp}',
            f'Очки перемещения: {sel_unit.moves}/{sel_unit.max_moves}',
            f'Мана: {sel_unit.mana}/{sel_unit.max_mana}',
            ]
    for i, to_print in enumerate(text):
        panel.blit(pg.font.Font(None, 25).render(to_print,
                                                 True,
                                                 colors['MediumSpringGreen']),
                   (10, 10 + i * 25))
    # Информация об игроке
    panel.blit(pg.font.Font(None, 25).render(f'Игрок {MOVE_COUNTER % 2 + 1}',
                                             True,
                                             colors['MediumSpringGreen']),
               (size[0] / 3, 10))
    panel.blit(pg.font.Font(None, 25).render(f'Монеты: {sel_player.money} квач',
                                             True,
                                             colors['MediumSpringGreen']),
               (size[0] / 3, 10 + 25))
    panel.blit(pg.font.Font(None, 25).render(f'Доход: {sel_player.income} квач в ход',
                                             True,
                                             colors['MediumSpringGreen']),
               (size[0] / 3, 10 + 25 * 2))
    # Информация о текущей клетке
    panel.blit(pg.font.Font(None, 25).render('Текущая клетка: ',
                                             True,
                                             colors['MediumSpringGreen']),
               (size[0] / 3 * 2, 10))
    hex_coord = point_in(sel_unit.coord_x, sel_unit.coord_y)
    panel.blit(pg.font.Font(None, 25).render(field.field[hex_coord[1]][hex_coord[0]][0],
                                             True,
                                             colors['MediumSpringGreen']),
               (size[0] / 3 * 2, 10 + 25))
    return panel


def button_draw(size: (int, int), form: str) -> pg.Surface:
    """
    Отрисовка кнопки
    :param size: размер кнопки
    :param form: тип кнопки
    :return: поверхность с отрисованной кнопкой
    """
    btn = pg.Surface(size)  # Поверхность кнопки
    btn.fill(colors['SaddleBrown'])  # Фоновый цвет
    pg.draw.circle(btn, colors['DarkGoldenRod'], (size[1] // 2, size[1] // 2), size[1] // 2)  # Круг
    if form == 'next':
        pg.draw.polygon(btn, colors['светло жёлтый'], [  # Треугольник
            [size[1] // 3, size[1] // 4],
            [size[1] // 3, size[1] // 4 * 3],
            [size[1] // 4 * 3, size[1] // 2],
        ])
        btn.blit(pg.font.Font(None, 20).render(f'Ход {MOVE_COUNTER}',  # Отрисовка счетчика хода
                                               True,
                                               colors['Black']),
                 (size[0] // 2 - 25, size[1] - 40))
    elif form == 'attack':
        img = pg.image.load('buttons/attack.png')  # Загрузка картинки
        img = pg.transform.scale(img, (int(size[1] / 1.4), int(size[1] / 1.5)))  # Масштабирование
        btn.blit(img, img.get_rect(bottomright=(size[1] // 1.2, size[1] // 1.2)))  # Отрисовка
    elif form == 'defense':
        # img = pg.image.load('buttons/defend.png')  # Загрузка картинки
        # img = pg.transform.scale(img, (int(size[1] / 1.3), int(size[1] / 1.3)))  # Масштабирование
        # btn.blit(img, img.get_rect(bottomright=(4.4 * size[1], int(3.6 * size[1]))))  # Отрисовка
        pass
    elif form == 'trade':
        img = pg.image.load('buttons/trade.png')  # Загрузка картинки
        img = pg.transform.scale(img, (int(size[1] / 1.1), int(size[1] / 1.1)))  # Масштабирование
        btn.blit(img, img.get_rect(bottomright=(0.95 * size[1], int(1.0 * size[1]))))  # Отрисовка
    elif form == 'select':
        # TODO картинка кнопки select
        # img = pg.image.load(path)  # Загрузка картинки
        # img = pg.transform.scale(img, size)  # Масштабирование
        # screen.blit(img, img.get_rect(bottomright=(w, h)))  # Отрисовка
        pass
    return btn


def main():
    """Главная функция кода"""
    pg.init()
    screen = pg.display.set_mode((screen_size[0], screen_size[1]))
    is_run = True
    med_bld = ['Небольшая мельница. Приносит 5 золота в ход.',
               'Изящная арка',
               'Кузница позволяет улучшать оружие и броню.',
               'Таверна.Ускоренная регенирация +10 hp',
               'Старое кладбище. Купите карту, чтобы найти сокровище',
               'Ферма. Приносит 10 золота в ход',
               'Таверна наёмников. Можно нанять войска',
               'Замок наёмников. Можно нанять усовершенствованные войска.',
               'Местная пекарня. Приносит 10 золота в ход',
               'Небольшой замок. Приносит 15 золота в ход',
               'Королевский замок. Приносит 15 золота в ход, можно нанимать войска',
               'Сокровище. 50 золота, +5 к силе оружия',
               'Золотой рудник. Приносит 20 золота в ход',
               'Башня магов. Можно нанять магов за золото и очки знаменитости',
               'Лагерь разбойников',
               ]
    print(med_bld)
    player1 = Player(100, [], [])
    player1.add_unit(
        Unit('Воин', 100, 0, 15, 0, 2, 10, int(3 * hex_size[0] / 2),
             int(hex_size[1] / 2), screen_size, field_size))
    player2 = Player(100, [], [])
    player2.add_unit(
        Unit('Воин', 100, 0, 15, 0, 2, 10, int(24 * hex_size[0] - hex_size[0] / 2),
             int(hex_size[1] / 2), screen_size, field_size))
    # Загрузка данных
    global field
    field = Field(screen_size, field_size)
    field.gen_given_field()
    now = 0
    attack = False
    while is_run:
        # Обработка событий
        global MOVE_COUNTER
        if MOVE_COUNTER % 2 == 0:
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
                # print(mouse_x, mouse_y)
            if event.type == pg.QUIT:
                is_run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                try:
                    mouse_hex_x, mouse_hex_y = mouse_in(mouse_x, mouse_y)
                except TypeError:
                    break
                unit_hex_x, unit_hex_y = point_in(unit.coord_x, unit.coord_y)
                if attack:
                    if unit_hex_y % 2 == 0:
                        centres = [(unit_hex_x - 1, unit_hex_y - 1),
                                   (unit_hex_x, unit_hex_y - 1),
                                   (unit_hex_x + 1, unit_hex_y),
                                   (unit_hex_x, unit_hex_y + 1),
                                   (unit_hex_x - 1, unit_hex_y + 1),
                                   (unit_hex_x - 1, unit_hex_y)]
                    else:
                        centres = [(unit_hex_x, unit_hex_y - 1),
                                   (unit_hex_x + 1, unit_hex_y - 1),
                                   (unit_hex_x + 1, unit_hex_y),
                                   (unit_hex_x + 1, unit_hex_y + 1),
                                   (unit_hex_x, unit_hex_y + 1),
                                   (unit_hex_x - 1, unit_hex_y)]
                    if any_on(mouse_hex_x, mouse_hex_y, enemy.units):
                        attacker = who_on(unit_hex_x, unit_hex_y, player.units)
                        enemy_unit = who_on(mouse_hex_x, mouse_hex_y, enemy.units)
                        attacker.attack(enemy_unit)
                        attack = False
                    else:
                        attack = False
                elif not attack:
                    # Нажатие на кнопку следующего хода
                    if (mouse_x - 1445) ** 2 + (mouse_y - 922) ** 2 < 57 ** 2:
                        MOVE_COUNTER += 1
                        now = 0
                        player.refresh()
                        # Отрисовка юнитов игрока 1
                        for i in range(len(player1.units)):
                            player1.units[i].refresh()

                        # Отрисовка юнитов игрока 2
                        for i in range(len(player2.units)):
                            player2.units[i].refresh()
                    # Нажатие на кнопку trade
                    elif (mouse_x - 1445) ** 2 + (mouse_y - 817) ** 2 < 57 ** 2:
                        if unit.moves > 0:
                            if field.field[unit_hex_y][unit_hex_x][0] == 'medieval':
                                if field.field[unit_hex_y][unit_hex_x][1] == 0:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 1:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 2:
                                    if player.money >= 20:
                                        if player.step_forge + 2 <= MOVE_COUNTER:
                                            unit.moves = 0
                                            unit.dmg += 5
                                            player.money -= 20
                                            player.step_forge = MOVE_COUNTER
                                elif field.field[unit_hex_y][unit_hex_x][1] == 3:
                                    if player.money >= 10:
                                        if player.chet_step + 1 <= MOVE_COUNTER:
                                            unit.moves -= 1
                                            player.money -= 10
                                            player.chet_step = MOVE_COUNTER
                                            if player.treasure_map == 0:
                                                # TODO say u find a map
                                                player.treasure_map = 1
                                elif field.field[unit_hex_y][unit_hex_x][1] == 4:
                                    if player.treasure_map == 1:
                                        player.money += 50
                                        player.treasure_map = -1

                                elif field.field[unit_hex_y][unit_hex_x][1] == 5:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 6:
                                    if player.money >= 50:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('Воин', 100, 0, 15, 0, 2, 10,
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 50
                                elif field.field[unit_hex_y][unit_hex_x][1] == 7:
                                    if player.money >= 50:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('Воин', 100, 0, 15, 0, 2, 10,
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 50
                                elif field.field[unit_hex_y][unit_hex_x][1] == 8:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 9:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 10:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 11:
                                    if player.big_treasure == 0:
                                        unit.moves = 0
                                        unit.dmg += 15
                                        player.money += 250
                                        player.big_treasure = -1
                                elif field.field[unit_hex_y][unit_hex_x][1] == 12:
                                    pass
                                elif field.field[unit_hex_y][unit_hex_x][1] == 13:
                                    if player.money >= 50:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('Воин', 100, 0, 15, 0, 2, 10,
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 50
                                elif field.field[unit_hex_y][unit_hex_x][1] == 14:
                                    pass

                    # Нажатие на кнопку переключения юнита
                    elif (mouse_x - 1330) ** 2 + (mouse_y - 817) ** 2 < 57 ** 2:
                        if MOVE_COUNTER % 2 == 0:
                            if now + 1 == len(player1.units):
                                now = 0
                            else:
                                now += 1
                            unit = player1.units[now]
                        else:
                            if now + 1 == len(player2.units):
                                now = 0
                            else:
                                now += 1
                            unit = player2.units[now]
                    # Нажатие на кнопку attack
                    elif (mouse_x - 1330) ** 2 + (mouse_y - 922) ** 2 < 57 ** 2:
                        if unit.moves > 0:
                            if how_much_on(unit_hex_x, unit_hex_y, player.units) == 1:
                                attack = True
                    else:
                        if unit.moves > 0:
                            # По часовой
                            if unit_hex_y % 2 == 0:
                                centres = [(unit_hex_x - 1, unit_hex_y - 1),
                                           (unit_hex_x, unit_hex_y - 1),
                                           (unit_hex_x + 1, unit_hex_y),
                                           (unit_hex_x, unit_hex_y + 1),
                                           (unit_hex_x - 1, unit_hex_y + 1),
                                           (unit_hex_x - 1, unit_hex_y)]
                            else:
                                centres = [(unit_hex_x, unit_hex_y - 1),
                                           (unit_hex_x + 1, unit_hex_y - 1),
                                           (unit_hex_x + 1, unit_hex_y),
                                           (unit_hex_x + 1, unit_hex_y + 1),
                                           (unit_hex_x, unit_hex_y + 1),
                                           (unit_hex_x - 1, unit_hex_y)]
                            stop = True
                            counter = 0
                            while stop:
                                if counter == 6:
                                    stop = False
                                    counter = 0
                                unit_hex_x_edited, unit_hex_y_edited = centres[counter]
                                coord_x, coord_y = center_hex(unit_hex_x_edited, unit_hex_y_edited)
                                if (mouse_x - coord_x) ** 2 + (mouse_y - coord_y) ** 2 < 30 ** 2:
                                    stop = False
                                    counter = 0
                                    if not any_on(unit_hex_x_edited,
                                                  unit_hex_y_edited,
                                                  player.units) and not any_on(unit_hex_x_edited,
                                                                               unit_hex_y_edited,
                                                                               enemy.units):
                                        unit.coord_x = coord_x
                                        unit.coord_y = coord_y
                                        unit.moves -= 1
                                        hex_x, hex_y = point_in(unit.coord_x, unit.coord_y)
                                        if field.field[hex_y][hex_x][0] == 'medieval':
                                            player.add_building(Building(
                                                hex_x,
                                                hex_y,
                                                field.field[unit_hex_y][unit_hex_x][1]))
                                else:
                                    counter += 1

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        field.draw(screen)
        for i in range(len(player1.units)):  # отображение юнитов игрока 1
            player1.units[i].draw(screen)

        for i in range(len(player2.units)):  # отображение юнитов игрока 2
            player2.units[i].draw(screen)

        # Отрисовка рамки вокруг вражеских и не ходивших юнитов
        if player == player1:
            tmp_col = colors['DeepSkyBlue'], colors['Red']
        else:
            tmp_col = colors['Red'], colors['DeepSkyBlue']
        for i in player1.units:
            pg.draw.polygon(screen, tmp_col[0], [
                (i.coord_x - hex_size[0] / 2, i.coord_y - hex_size[1] / 4),
                (i.coord_x, i.coord_y - hex_size[1] / 2),
                (i.coord_x + hex_size[0] / 2, i.coord_y - hex_size[1] / 4),
                (i.coord_x + hex_size[0] / 2, i.coord_y + hex_size[1] / 4),
                (i.coord_x, i.coord_y + hex_size[1] / 2),
                (i.coord_x - hex_size[0] / 2, i.coord_y + hex_size[1] / 4),
            ], 3)
        for i in player2.units:
            pg.draw.polygon(screen, tmp_col[1], [
                (i.coord_x - hex_size[0] / 2, i.coord_y - hex_size[1] / 4),
                (i.coord_x, i.coord_y - hex_size[1] / 2),
                (i.coord_x + hex_size[0] / 2, i.coord_y - hex_size[1] / 4),
                (i.coord_x + hex_size[0] / 2, i.coord_y + hex_size[1] / 4),
                (i.coord_x, i.coord_y + hex_size[1] / 2),
                (i.coord_x - hex_size[0] / 2, i.coord_y + hex_size[1] / 4),
            ], 3)
        # Отрисовка рамки выбранного юнита
        pg.draw.polygon(screen, colors['Yellow'], [
            (unit.coord_x - hex_size[0] / 2, unit.coord_y - hex_size[1] / 4),
            (unit.coord_x, unit.coord_y - hex_size[1] / 2),
            (unit.coord_x + hex_size[0] / 2, unit.coord_y - hex_size[1] / 4),
            (unit.coord_x + hex_size[0] / 2, unit.coord_y + hex_size[1] / 4),
            (unit.coord_x, unit.coord_y + hex_size[1] / 2),
            (unit.coord_x - hex_size[0] / 2, unit.coord_y + hex_size[1] / 4),
        ], 3)

        panel_coord = (0, 750)  # Координаты панели управления
        # Отрисовка панели управления
        screen.blit(panel_draw(panel_size, unit, player), panel_coord)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)
    sys.exit()


if __name__ == '__main__':
    main()
