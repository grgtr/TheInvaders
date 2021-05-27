"""Модуль игрока"""


class Player:
    """Класс игрока"""

    def __init__(self, money: int, units, buildings):
        self.money = money
        self.units = units
        self.buildings = buildings
        self.power = 0
        self.step_tavern = 0
        self.step_forge = 0
        self.chet_step = 0
        self.now_step = 0
        self.treasure_map = 0
        self.income = 0
        self.big_treasure = 0

    def add_unit(self, unit) -> None:
        """Добавление юнита"""
        self.units.append(unit)

    def add_building(self, building) -> None:
        """Добавление строения"""
        self.buildings.append(building)
        self.revenue()

    def revenue(self) -> None:
        """Увеличение дохода"""
        self.income = 0
        for i in range(len(self.buildings)):
            # print(self.buildings[i].index)
            if self.buildings[i].index == 0:
                self.income += 5
            elif self.buildings[i].index == 5:
                self.income += 10
            elif self.buildings[i].index == 8:
                self.income += 10
            elif self.buildings[i].index == 9:
                self.income += 15
            elif self.buildings[i].index == 10:
                self.income += 15
            elif self.buildings[i].index == 12:
                self.income += 20
        # print(self.income)

    def refresh(self) -> None:
        """Добавление денег после хода"""
        self.money += self.income
