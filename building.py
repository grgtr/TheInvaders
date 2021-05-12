"""Модуль строения"""


class Building:
    """Класс строения"""
    def __init__(self, hex_x, hex_y, index):
        self.hex_x = hex_x
        self.hex_y = hex_y
        self.index = index
        self.player = 0
