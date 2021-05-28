"""Модуль юнитов"""
import pygame as pg


class Unit:
    """Класс игровых юнитов"""
    def __init__(self, title: str, x: int, y: int, screen_size: (int, int), field_size: (int, int)):
        self.title = title
        # self.max_hp = hp  # Максимальное количество здоровья
        # self.health = hp  # Здоровье
        # self.regen = regen
        # self.lvl = 0  # Уровень
        # self.exp = 0  # Опыт
        # self.max_mana = mana  # Максимальное количество маны
        # self.mana = 0  # Количество маны
        # self.dmg = dmg  # Урон
        # self.defense = defense  # Защита
        # self.max_moves = moves  # Максимальное количество очков перемещения
        # self.moves = moves  # Количество очков перемещения
        self.coord_x = x
        self.coord_y = y
        if self.title == 'knight':
            self.max_hp = 150  # Максимальное количество здоровья
            self.health = 150  # Здоровье
            self.regen = 15
            self.lvl = 1  # Уровень
            self.exp = 0  # Опыт
            self.max_mana = 0  # Максимальное количество маны
            self.max_dmg = 60
            self.dmg = 60  # Урон
            self.defense = 0  # Защита
            self.max_moves = 2  # Максимальное количество очков перемещения
            self.moves = 2  # Количество очков перемещения
            self.image = pg.image.load('units/knight/standing/standing05.png')
        elif self.title == 'wizard':
            self.max_hp = 90  # Максимальное количество здоровья
            self.health = 90  # Здоровье
            self.regen = 15
            self.lvl = 1  # Уровень
            self.exp = 0  # Опыт
            self.max_dmg = 80
            self.dmg = 80  # Урон
            self.defense = 0  # Защита
            self.max_moves = 2  # Максимальное количество очков перемещения
            self.moves = 2  # Количество очков перемещения
            self.image = pg.image.load('units/wizard/standing/standing_04.png')  # Картинка мага
        elif self.title == 'elf':
            self.max_hp = 120  # Максимальное количество здоровья
            self.health = 120  # Здоровье
            self.regen = 15
            self.lvl = 1  # Уровень
            self.exp = 0  # Опыт
            self.max_mana = 0  # Максимальное количество маны
            self.max_dmg = 60
            self.dmg = 60  # Урон
            self.defense = 0  # Защита
            self.max_moves = 3  # Максимальное количество очков перемещения
            self.moves = 3  # Количество очков перемещения
            self.image = pg.image.load('units/elf/standing/elf_00.png')
        self.hex_size = (screen_size[0] // field_size[0],  # Размер гекса (120, 140)
                         screen_size[1] // field_size[1])
        self.image = pg.transform.scale(self.image, self.hex_size)  # Масштабирование

    def draw(self, screen) -> None:
        """Отрисовка юнита"""

        screen.blit(self.image,  # Отрисовка
                    self.image.get_rect(bottomright=(self.coord_x + self.hex_size[1] // 2,
                                                     self.coord_y + self.hex_size[0] // 2)))

    def refresh(self) -> None:
        """Обновление перед ходом"""
        # Регенерация
        if (self.health != self.max_hp) and ((self.health + self.regen) <= self.max_hp):
            self.health += self.regen
        elif (self.health + self.regen) > self.max_hp:
            self.health = self.max_hp
        self.mana = self.max_mana  # Восстановление маны
        self.moves = self.max_moves  # Восстановление очков перемещения

    def attack(self, enemy) -> None:
        """
        Атака
        :param enemy: кого атакуют
        :return:
        """
        enemy: Unit
        enemy.health -= self.dmg * ((100 + -1 * enemy.defense * 20) / 100)  # Нанесение урона
        self.moves = 0  # Обнуление очков перемещения
        if not enemy.is_alive():  # Если противник побежден
            self.exp += 50 // (self.lvl + 1) ** 0.5  # Получение опыта
            self.check()  # Проверка на новый уровень
        else:  # Если противник не побежден
            if self.title != 'elf':
                self.health -= enemy.dmg * ((100 + enemy.defense * 20) / 100) // 2  # Нанесение ответного урона
            if not self.is_alive():  # Если юнит погиб
                enemy.exp += 50 // enemy.lvl ** 0.5  # Получение противником опыта
                enemy.check()  # Проверка на новый уровень

    def defend(self, protect: int) -> None:
        """Защита"""
        if self.moves != 0:
            self.defend += protect
            self.moves = 0

    def check(self) -> None:
        """Проверка на вшивость"""
        # Получен ли уровень
        self.dmg = self.max_dmg * (self.health / self.max_hp)
        if self.exp >= 100:
            self.lvl += 1
            self.exp -= 100

    def is_alive(self) -> bool:
        """Жив ли юнит"""
        return self.health > 0

    def movement(self) -> bool:
        """Проверка на возможность перемещения"""
        return self.moves > 0
