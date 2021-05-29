"""Главный модуль программы"""

import sys
import pygame as pg
from field import Field
from unit import Unit
from building import Building
from player import Player

field_size = 25, 14
hex_size = 60, 70  # Размер гексов (6:7)
screen_size = width, height = field_size[0] * hex_size[0], \
                              field_size[1] * hex_size[1]  # Размер экрана
FIELD: Field
colors = {
    'White': (255, 255, 255),
    'Black': (0, 0, 0),
    'DarkGoldenRod': (184, 134, 11),
    'Tan': (210, 180, 140),
    'SaddleBrown': (139, 69, 19),
    'светло-жёлтый': (255, 217, 73),
    'MediumSpringGreen': (0, 250, 154),
    'Yellow': (255, 255, 0),
    'Red': (255, 0, 0),
    'DeepSkyBlue': (0, 191, 255),
    'Lime': (0, 255, 0),
    'Salmon': (250, 128, 114),
    'LightBlue': (173, 216, 230),
}
FONT = 'font.ttf'
MOVE_COUNTER = 0  # Счетчик ходов
panel_size = (screen_size[0], 230)  # Размер панели управления


def fixed(num_obj, digits=0):
    """Фиксированной количество знаков после запятой"""
    return f"{num_obj:.{digits}f}"


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


def how_much_on(hex_x, hex_y, units) -> int:
    """Проверка количества юнитов на клетке"""
    count = 0
    for i in range(len(units)):
        uhx, uhy = point_in(units[i].coord_x, units[i].coord_y)
        if hex_x == uhx and hex_y == uhy:
            count += 1
    return count


def whose_build(build, player, enemy) -> int:
    """Определение, какому игроку принадлежит постройка"""
    for i in player.buildings:
        if i.hex_x == build.hex_x and i.hex_y == build.hex_y:
            return -1
    for i in range(len(enemy.buildings)):
        if enemy.buildings[i].hex_x == build.hex_x and enemy.buildings[i].hex_y == build.hex_y:
            return i
    return -2


def number_unit(enemy_unit, enemy) -> int:
    """Поиск юнита по координатам"""
    for i in range(len(enemy.units)):
        if (enemy_unit.coord_x == enemy.units[i].coord_x
                and enemy_unit.coord_y == enemy.units[i].coord_y):
            return i
    return -2


def defense(cell) -> int:
    """Модификатор защиты клетки"""
    if cell[0] == 'medieval':
        if cell[1] == 0:
            return 0
        if cell[1] == 1:
            return 0
        if cell[1] == 2:
            return 1
        if cell[1] == 3:
            return 1
        if cell[1] == 4:
            return 0
        if cell[1] == 5:
            return 1
        if cell[1] == 6:
            return 1
        if cell[1] == 7:
            return 3
        if cell[1] == 8:
            return 0
        if cell[1] == 9:
            return 2
        if cell[1] == 10:
            return 2
        if cell[1] == 11:
            return 0
        if cell[1] == 12:
            return 0
        if cell[1] == 13:
            return 0
        if cell[1] == 14:
            return 1
    if cell[0] == 'grass':
        if cell[1] == 0:
            return -2
        if cell[1] == 1:
            return -1
        if cell[1] == 2:
            return -1
        if cell[1] == 3:
            return 1
        if cell[1] == 4:
            return 1
        if cell[1] == 5:
            return 1
        if cell[1] == 6:
            return 1
        if cell[1] == 7:
            return 1
    if cell[0] == 'dirt':
        if cell[1] == 0:
            return -2
        if cell[1] == 1:
            return -1
        if cell[1] == 2:
            return -1
        if cell[1] == 3:
            return 1
        if cell[1] == 4:
            return 1
        if cell[1] == 5:
            return 1
        if cell[1] == 6:
            return 1
        if cell[1] == 7:
            return 1
        if cell[1] == 8:
            return 2
    return 0


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
    med_bld = ['Небольшая мельница. Приносит 5 золота в ход',  # Подписи к клеткам
               'Изящная арка',
               'Кузница позволяет улучшать оружие за 50 квач',
               'Таверна.Ускоренная регенерация +10 hp',
               'Старое кладбище. Купите карту, чтобы найти сокровище',
               'Ферма. Приносит 10 квач в ход',
               'Таверна наёмников. Можно нанимать рыцарей за 250 квач',
               'Королевский замок. Можно нанимать рыцарей за 250 квач, даёт монеты',
               'Местная пекарня. Приносит 10 квач в ход. Можно нанять эльфов-лучников за 250 квач',
               'Небольшой замок. Приносит 15 квач в ход. Можно нанять эльфов-лучников за 250 квач',
               'Замок наёмников. Приносит 15 квач в ход. Можно нанимать рыцарей за 250 квач',
               'Сокровище. 250 золота, +15 к силе оружия',
               'Золотой рудник. Приносит 20 квач в ход',
               'Башня магов. Можно нанять магов за 300 квач',
               'Лагерь разбойников. Можно захватить и нанять эльфов-лучников за 250 квач',
               ]
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
            f'Здоровье: {fixed(sel_unit.health, 2)}/{sel_unit.max_hp}',
            f'Сила атаки: {fixed(sel_unit.dmg, 2)}',
            f'Защита: {sel_unit.defense}',
            f'Уровень: {sel_unit.lvl + 1}',
            f'Опыт: {sel_unit.exp}',
            f'Очки действий: {sel_unit.moves}/{sel_unit.max_moves}',
            ]
    for i, to_print in enumerate(text):
        panel.blit(pg.font.Font(FONT, 25).render(to_print,
                                                 True,
                                                 colors['светло-жёлтый']),
                   (10, 10 + i * 25))
    # Информация об игроке
    panel.blit(pg.font.Font(FONT, 25).render(f'Игрок: {MOVE_COUNTER % 2 + 1}',
                                             True,
                                             colors['светло-жёлтый']),
               (size[0] / 4, 10 + 25 * 5))
    panel.blit(pg.font.Font(FONT, 25).render(f'Монеты: {sel_player.money} квач',
                                             True,
                                             colors['светло-жёлтый']),
               (size[0] / 4, 10 + 25 * 6))
    panel.blit(pg.font.Font(FONT, 25).render(f'Доход: {sel_player.income} квач в ход',
                                             True,
                                             colors['светло-жёлтый']),
               (size[0] / 4, 10 + 25 * 7))
    # Информация о текущей клетке
    panel.blit(pg.font.Font(FONT, 25).render('Текущая клетка: ',
                                             True,
                                             colors['светло-жёлтый']),
               (size[0] / 4, 10))
    hex_coord = point_in(sel_unit.coord_x, sel_unit.coord_y)
    # Информация о клетке
    if FIELD.field[hex_coord[1]][hex_coord[0]][0] == 'medieval':
        panel.blit(pg.font.Font(FONT, 25).render(
            med_bld[FIELD.field[hex_coord[1]][hex_coord[0]][1]],
            True,
            colors['светло-жёлтый']),
            (size[0] / 4, 10 + 25))
        panel.blit(pg.font.Font(FONT, 25).render('Модификатор обороны: ' + str(
            defense(FIELD.field[hex_coord[1]][hex_coord[0]])),
                                                 True,
                                                 colors['светло-жёлтый']),
                   (size[0] / 4, 10 + 25 + 25))
        if sel_player.treasure_map == 1 and FIELD.field[hex_coord[1]][hex_coord[0]][1] == 3:
            panel.blit(pg.font.Font(FONT, 25).render(
                'Вы нашли карту сокровищ. В таверне говорят, '
                'что на местном кладбище спрятано золото',
                True,
                colors['светло-жёлтый']),
                (size[0] / 4, 10 + 25 + 25 + 25))

    else:
        panel.blit(pg.font.Font(FONT, 25).render('Модификатор обороны: ' + str(
            defense(FIELD.field[hex_coord[1]][hex_coord[0]])),
                                                 True,
                                                 colors['светло-жёлтый']),
                   (size[0] / 4, 10 + 25))
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
        pg.draw.polygon(btn, colors['светло-жёлтый'], [  # Треугольник
            [size[1] // 3, size[1] // 4],
            [size[1] // 3, size[1] // 4 * 3],
            [size[1] // 4 * 3, size[1] // 2],
        ])
        btn.blit(pg.font.Font(FONT, 20).render(f'Ход: {MOVE_COUNTER}',  # Отрисовка счетчика хода
                                               True,
                                               colors['Black']),
                 (size[0] // 2 - 22, size[1] - 29))
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
        img = pg.image.load('buttons/select.png')  # Загрузка картинки
        img = pg.transform.scale(img, (int(size[1] / 1.1), int(size[1] / 1.1)))  # Масштабирование
        btn.blit(img, img.get_rect(bottomright=(0.95 * size[1], int(1.0 * size[1]))))  # Отрисовка
    return btn


def game(screen: pg.Surface):
    """Функция игры"""
    is_run = True
    player1 = Player(100, [], [])
    player1.add_unit(
        Unit('knight', int(3 * hex_size[0] / 2),
             int(hex_size[1] / 2), screen_size, field_size))
    player2 = Player(100, [], [])
    player2.add_unit(
        Unit('knight', int(24 * hex_size[0] - hex_size[0] / 2),
             int(hex_size[1] / 2), screen_size, field_size))
    # Загрузка данных
    global FIELD
    FIELD = Field(screen_size, field_size)
    FIELD.gen_given_field()
    now = 0
    attack = False
    while is_run:
        # Обработка событий
        global MOVE_COUNTER
        if MOVE_COUNTER % 2 == 0:
            enemy = player2
            player = player1
            try:
                unit = player1.units[now]
            except IndexError:
                print('error')
        else:
            enemy = player1
            player = player2
            try:
                unit = player2.units[now]
            except IndexError:
                print('error')
        for i in player.units:
            hex_x, hex_y = point_in(i.coord_x, i.coord_y)
            i.defense = defense(FIELD.field[hex_y][hex_x])
        for i in enemy.units:
            hex_x, hex_y = point_in(i.coord_x, i.coord_y)
            i.defense = defense(FIELD.field[hex_y][hex_x])
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos

            if event.type == pg.QUIT:
                is_run = False
                sys.exit()
            if event.type == pg.KEYDOWN:
                keys = pg.key.get_pressed()
                if keys[pg.K_a] and keys[pg.K_m]:  # Чит на ходы и деньги
                    player.money += 1000
                    unit.moves += 100
                elif keys[pg.K_m]:
                    unit.moves += 100
                if keys[pg.K_w]:
                    print(7878)
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
                    for i in centres:
                        if mouse_hex_x == i[0] and mouse_hex_y == i[1]:
                            if any_on(mouse_hex_x, mouse_hex_y, enemy.units):
                                attacker = who_on(unit_hex_x, unit_hex_y, player.units)
                                enemy_unit = who_on(mouse_hex_x, mouse_hex_y, enemy.units)
                                attacker.attack(enemy_unit)
                                if not enemy_unit.is_alive():
                                    position = number_unit(enemy_unit, enemy)
                                    if position != -2:
                                        attacker.coord_x = enemy_unit.coord_x
                                        attacker.coord_y = enemy_unit.coord_y
                                        enemy.units.pop(position)
                                        # Проверка на победу
                                        if len(player2.units) == 0:
                                            return 'game_over_win1'
                                        if len(player1.units) == 0:
                                            return 'game_over_win2'
                                        hex_x, hex_y = point_in(attacker.coord_x, attacker.coord_y)
                                        if FIELD.field[hex_y][hex_x][0] == 'medieval':
                                            print(hex_x, hex_y, FIELD.field[hex_y][hex_x][1])
                                            whose = whose_build(Building(hex_x, hex_y,
                                                                         FIELD.field[hex_y][hex_x][1]),
                                                                player, enemy)
                                            # print(whose, 'whose')
                                            if whose == -2:
                                                player.add_building(Building(
                                                    hex_x,
                                                    hex_y,
                                                    FIELD.field[hex_y][hex_x][1]))
                                                print(hex_x, hex_y, FIELD.field[hex_y][hex_x][1])
                                            elif whose == -1:
                                                pass
                                            else:
                                                print(player.buildings)
                                                print(enemy.buildings)
                                                player.add_building(Building(
                                                    hex_x,
                                                    hex_y,
                                                    FIELD.field[hex_y][hex_x][1]))
                                                # print(hex_x, hex_y, field.field[hex_y][hex_x][1])
                                                enemy.buildings.pop(whose)

                                            print(player.buildings)
                                            print(enemy.buildings)
                                            player.refresh()
                                            player.money -= player.income
                                            enemy.refresh()
                                            enemy.money -= enemy.income

                                if not attacker.is_alive():
                                    position = number_unit(attacker, player)
                                    if position != -2:
                                        player.units.pop(position)
                                        # Проверка на победу
                                        if len(player2.units) == 0:
                                            return 'game_over_win1'
                                        if len(player1.units) == 0:
                                            return 'game_over_win2'

                    attack = False
                elif not attack:
                    # Нажатие на кнопку следующего хода
                    if (mouse_x - 1445) ** 2 + (mouse_y - 922) ** 2 < 57 ** 2:
                        player.refresh()
                        player.revenue()
                        enemy.revenue()
                        MOVE_COUNTER += 1
                        now = 0
                        # Отрисовка юнитов игрока 1
                        for i in range(len(player1.units)):
                            player1.units[i].refresh()

                        # Отрисовка юнитов игрока 2
                        for i in range(len(player2.units)):
                            player2.units[i].refresh()
                    # Нажатие на кнопку trade
                    elif (mouse_x - 1445) ** 2 + (mouse_y - 817) ** 2 < 57 ** 2:
                        if unit.moves > 0:
                            if FIELD.field[unit_hex_y][unit_hex_x][0] == 'medieval':
                                if FIELD.field[unit_hex_y][unit_hex_x][1] == 0:
                                    pass
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 1:
                                    pass
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 2:  # Кузница
                                    if player.money >= 50:
                                        if player.step_forge + 2 <= MOVE_COUNTER:
                                            unit.moves = 0
                                            unit.max_dmg += 5
                                            player.money -= 50
                                            player.step_forge = MOVE_COUNTER
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 3:
                                    if player.money >= 10:
                                        if player.chet_step + 1 <= MOVE_COUNTER:
                                            if unit.health - 10 <= unit.max_hp:
                                                unit.health += 30
                                                player.money -= 10
                                                unit.moves -= 1
                                            player.chet_step = MOVE_COUNTER
                                            if player.treasure_map == 0:
                                                # print('treasure_map++')
                                                player.treasure_map = 1
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 4:
                                    if player.treasure_map == 1:
                                        player.money += 250
                                        player.treasure_map = -1

                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 5:
                                    pass
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 6:
                                    if player.money >= 250:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('knight',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 250
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 7:
                                    if player.money >= 250:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('knight',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 250
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 8:
                                    if player.money >= 250:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('elf',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 200
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 9:
                                    if player.money >= 200:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('elf',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 200
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 10:
                                    if player.money >= 250:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('knight',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 250
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 11:
                                    if player.big_treasure == 0:
                                        unit.moves = 0
                                        unit.max_dmg += 15
                                        player.money += 250
                                        player.big_treasure = -1
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 12:
                                    pass
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 13:
                                    if player.money >= 300:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('wizard',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 100
                                elif FIELD.field[unit_hex_y][unit_hex_x][1] == 14:
                                    if player.money >= 250:
                                        unit.moves -= 1
                                        coord_x, coord_y = center_hex(unit_hex_x, unit_hex_y)
                                        player.add_unit(
                                            Unit('elf',
                                                 coord_x, coord_y, screen_size, field_size))
                                        player.money -= 200

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
                                        if FIELD.field[hex_y][hex_x][0] == 'medieval':
                                            print(hex_x, hex_y, FIELD.field[hex_y][hex_x][1])
                                            whose = whose_build(Building(hex_x, hex_y,
                                                                         FIELD.field[hex_y][hex_x][1]),
                                                                player, enemy)
                                            # print(whose, 'whose')
                                            if whose == -2:
                                                player.add_building(Building(
                                                    hex_x,
                                                    hex_y,
                                                    FIELD.field[hex_y][hex_x][1]))
                                                print(hex_x, hex_y, FIELD.field[hex_y][hex_x][1])
                                            elif whose == -1:
                                                pass
                                            else:
                                                print(player.buildings)
                                                print(enemy.buildings)
                                                player.add_building(Building(
                                                    hex_x,
                                                    hex_y,
                                                    FIELD.field[hex_y][hex_x][1]))
                                                # print(hex_x, hex_y, field.field[hex_y][hex_x][1])
                                                enemy.buildings.pop(whose)

                                            print(player.buildings)
                                            print(enemy.buildings)
                                            player.refresh()
                                            player.money -= player.income
                                            enemy.refresh()
                                            enemy.money -= enemy.income
                                else:
                                    counter += 1

        # Отрисовка кадра
        screen.fill((255, 255, 255))  # Белый фон, рисуется первым!
        FIELD.draw(screen)
        for i in range(len(player1.units)):  # отображение юнитов игрока 1
            player1.units[i].draw(screen)
            player1.units[i].check()

        for i in range(len(player2.units)):  # отображение юнитов игрока 2
            player2.units[i].draw(screen)
            player2.units[i].check()

        panel_coord = (0, 750)  # Координаты панели управления
        # Отрисовка панели управления
        screen.blit(panel_draw(panel_size, unit, player), panel_coord)

        # Отрисовка рамки вокруг вражеских и не ходивших юнитов
        # Полоски их здоровья
        # И зданий
        if player == player1:
            tmp_col = colors['DeepSkyBlue'], colors['Red']
        else:
            tmp_col = colors['Red'], colors['DeepSkyBlue']
        for i in player.buildings:
            cor_x, cor_y = center_hex(i.hex_x, i.hex_y)
            pg.draw.polygon(screen, colors['LightBlue'], [
                (cor_x - hex_size[0] // 2, cor_y - hex_size[1] // 4 - 3),
                (cor_x, cor_y - hex_size[1] // 2 - 3),
                (cor_x + hex_size[0] // 2, cor_y - hex_size[1] // 4 - 3),
                (cor_x + hex_size[0] // 2, cor_y + hex_size[1] // 4 - 3),
                (cor_x, cor_y + hex_size[1] // 2 - 4),
                (cor_x - hex_size[0] // 2, cor_y + hex_size[1] // 4 - 3),
            ], 3)

        for i in enemy.buildings:
            cor_x, cor_y = center_hex(i.hex_x, i.hex_y)
            pg.draw.polygon(screen, colors['Salmon'], [
                (cor_x - hex_size[0] // 2, cor_y - hex_size[1] // 4 - 3),
                (cor_x, cor_y - hex_size[1] // 2 - 4),
                (cor_x + hex_size[0] // 2, cor_y - hex_size[1] // 4 - 3),
                (cor_x + hex_size[0] // 2, cor_y + hex_size[1] // 4 - 3),
                (cor_x, cor_y + hex_size[1] // 2 - 4),
                (cor_x - hex_size[0] // 2, cor_y + hex_size[1] // 4 - 3),
            ], 3)

        for i in player1.units:
            pg.draw.polygon(screen, tmp_col[0], [
                (i.coord_x - hex_size[0] // 2, i.coord_y - hex_size[1] // 4 - 3),
                (i.coord_x, i.coord_y - hex_size[1] // 2 - 3),
                (i.coord_x + hex_size[0] // 2, i.coord_y - hex_size[1] // 4 - 3),
                (i.coord_x + hex_size[0] // 2, i.coord_y + hex_size[1] // 4 - 3),
                (i.coord_x, i.coord_y + hex_size[1] // 2 - 4),
                (i.coord_x - hex_size[0] // 2, i.coord_y + hex_size[1] // 4 - 3),
            ], 3)
            # Рамка здоровья
            pg.draw.rect(screen, colors['Black'], (i.coord_x - 26, i.coord_y + 39, 52, 8), 2)
            # Шкала здоровья
            pg.draw.rect(screen, colors['Lime'],
                         (i.coord_x - 25, i.coord_y + 40, 50 / i.max_hp * i.health, 6), 0)
        for i in player2.units:
            pg.draw.polygon(screen, tmp_col[1], [
                (i.coord_x - hex_size[0] // 2, i.coord_y - hex_size[1] // 4 - 3),
                (i.coord_x, i.coord_y - hex_size[1] // 2 - 3),
                (i.coord_x + hex_size[0] // 2, i.coord_y - hex_size[1] // 4 - 3),
                (i.coord_x + hex_size[0] // 2, i.coord_y + hex_size[1] // 4 - 3),
                (i.coord_x, i.coord_y + hex_size[1] // 2 - 3),
                (i.coord_x - hex_size[0] // 2, i.coord_y + hex_size[1] // 4 - 3),
            ], 3)
            # Рамка здоровья
            pg.draw.rect(screen, colors['Black'], (i.coord_x - 26, i.coord_y + 39, 52, 8), 2)
            # Шкала здоровья
            pg.draw.rect(screen, colors['Lime'],
                         (i.coord_x - 25, i.coord_y + 40, 50 / i.max_hp * i.health, 6), 0)
        # Отрисовка рамки выбранного юнита
        pg.draw.polygon(screen, colors['Yellow'], [
            (unit.coord_x - hex_size[0] // 2, unit.coord_y - hex_size[1] // 4 - 3),
            (unit.coord_x, unit.coord_y - hex_size[1] // 2 - 3),
            (unit.coord_x + hex_size[0] // 2, unit.coord_y - hex_size[1] // 4 - 3),
            (unit.coord_x + hex_size[0] // 2, unit.coord_y + hex_size[1] // 4 - 3),
            (unit.coord_x, unit.coord_y + hex_size[1] // 2 - 3),
            (unit.coord_x - hex_size[0] // 2, unit.coord_y + hex_size[1] // 4 - 3),
        ], 3)

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)


def menu(screen: pg.Surface) -> str:
    """Функция меню"""
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (580 < mouse_x < 900) \
                        and (355 < mouse_y < 465):  # Нажатие кнопки ИГРАТЬ
                    return 'game'
                if (580 < mouse_x < 900) \
                        and (480 < mouse_y < 585):  # Нажатие кнопки ПРАВИЛА
                    return 'how_to_play'
                if (580 < mouse_x < 900) \
                        and (595 < mouse_y < 705):  # Нажатие кнопки АВТОРЫ
                    return 'authors'
                if (580 < mouse_x < 900) \
                        and (715 < mouse_y < 825):  # Нажатие кнопки ВЫХОД
                    return 'quit'

        background_img = pg.image.load('background/background1500x980.png')  # Загрузка картинки
        screen.blit(background_img, background_img.get_rect(bottomright=(1500, 980)))  # Отрисовка
        menu_img = pg.image.load('background/main_menu1500x980.png')  # Загрузка картинки
        screen.blit(menu_img, menu_img.get_rect(bottomright=(1500, 980)))  # Отрисовка

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)


def authors(screen: pg.Surface):
    """Экран авторов проекта"""
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (580 < mouse_x < 900) \
                        and (715 < mouse_y < 825):  # Нажатие кнопки НАЗАД
                    return 'menu'

        background_img = pg.image.load('background/background1500x980.png')  # Загрузка картинки
        screen.blit(background_img, background_img.get_rect(bottomright=(1500, 980)))  # Отрисовка
        athers_img = pg.image.load('background/authors1500x980.png')  # Загрузка картинки
        screen.blit(athers_img, athers_img.get_rect(bottomright=(1500, 980)))  # Отрисовка

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)


def game_over(screen: pg.Surface, text: str):
    """Экран конца игры"""
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (580 < mouse_x < 900) \
                        and (715 < mouse_y < 825):  # Нажатие кнопки ВЫХОД
                    return 'menu'

        background_img = pg.image.load('background/background1500x980.png')  # Загрузка картинки
        screen.blit(background_img, background_img.get_rect(bottomright=(1500, 980)))  # Отрисовка
        if text == '1':
            # Загрузка картинки 1
            game_over_img = pg.image.load('background/game_over_1_1500x980.png')
        else:
            # Загрузка картинки 2
            game_over_img = pg.image.load('background/game_over_2_1500x980.png')
        screen.blit(game_over_img, game_over_img.get_rect(bottomright=(1500, 980)))  # Отрисовка

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)


def how_to_play(screen: pg.Surface):
    """Экран как играть"""
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            if event.type == pg.QUIT:
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if (627 < mouse_x < 870) \
                        and (890 < mouse_y < 970):  # Нажатие кнопки ВЫХОД
                    return 'menu'

        background_img = pg.image.load('background/background1500x980.png')  # Загрузка картинки
        screen.blit(background_img, background_img.get_rect(bottomright=(1500, 980)))  # Отрисовка
        rulles_img = pg.image.load('background/rules1500x980.png')  # Загрузка картинки
        screen.blit(rulles_img, rulles_img.get_rect(bottomright=(1500, 980)))  # Отрисовка

        # Подтверждение отрисовки и ожидание
        pg.display.flip()
        pg.time.wait(10)


def main():
    """Главная функция кода"""
    pg.init()
    mysound = pg.mixer.Sound('music.wav')  # Загрузка трека
    mysound.play(loops=10000000)
    screen = pg.display.set_mode((screen_size[0], screen_size[1]))
    command = menu(screen)
    while True:
        if command == 'menu':
            command = menu(screen)
        if command == 'game':
            command = game(screen)
        elif command == 'authors':
            command = authors(screen)
        elif command == 'quit':
            sys.exit()
        elif command == 'game_over_win1':
            command = game_over(screen, 'Выиграл игрок 1')
        elif command == 'game_over_win2':
            command = game_over(screen, 'Выиграл игрок 2')
        elif command == 'how_to_play':
            command = how_to_play(screen)


if __name__ == '__main__':
    main()
