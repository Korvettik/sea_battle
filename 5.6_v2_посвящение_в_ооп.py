from random import randint, choice

class Ship:
    def __init__(self, length, tp=1, x=None, y=None):
        self._x = x  # [0 - 9] слева направо
        self._y = y  # [0 - 9] сверху вниз
        self._length = length  # 1, 2, 3, 4
        self._tp = tp  # 1-horizont, 2-vertical
        self._is_move = True
        self._cells = [1 for i in range(self._length)]

    def set_start_coords(self, x, y):
        self._x = x
        self._y = y

    def get_start_coords(self):
        return self._x, self._y

    def move(self, go):
        if self._is_move == True:

            if self._tp == 1:  # horizont
                if go > 0:
                    self._x += abs(go)
                else:
                    self._x -= abs(go)

            if self._tp == 2:  # vertical
                if go > 0:
                    self._y += abs(go)  # ВНИЗ
                else:
                    self._y -= abs(go)  # ВВЕРХ

        else:
            pass  # не перемещаем (заблокировано - судно подбито)



    def is_collide(self, ship):
        # сформируем список кортежей координат самого корабля и поля вокруг него.
        # если этот список не содержит списка кортежей коорданат подаваемого корабля,
        # то False, иначе True

        self_matrix = []
        ship_matrix = []

        #для себя
        if self._tp == 1:  # horizont
            x_start = self._x - 1  # шире на 1 влево
            x_stop = self._x + self._length  # шире на 1 вправо
            y_start = self._y - 1  # выше на 1 вверх
            y_stop = self._y + 1  # ниже на 1 вниз

            for y in range(y_start, y_stop + 1):  # от 0 к 9 вниз
                for x in range(x_start, x_stop + 1):  # от 0 к 9 вправо
                    self_matrix.append((x, y))

        if self._tp == 2:  # vertical
            x_start = self._x - 1  # шире на 1 влево
            x_stop = self._x + 1  # шире на 1 вправо
            y_start = self._y - 1  # выше на 1 вверх
            y_stop = self._y + self._length  # ниже на 1 вниз

            for y in range(y_start, y_stop + 1):  # от 0 к 9 вниз
                for x in range(x_start, x_stop + 1):  # от 0 к 9 вправо
                    self_matrix.append((x, y))

        # для корабля
        if ship._tp == 1:  # horizont
            sx_start = ship._x # ширина влево вровень
            sx_stop = ship._x + ship._length - 1  # ширина вправо вровень
            sy_start = ship._y  # высота вровень

            for x in range(sx_start, sx_stop+1):
                ship_matrix.append((x, sy_start))

        if ship._tp == 2:  # vertical
            sx_start = ship._x  # ширина вровень
            sy_start = ship._y  # высота вверх вровень
            sy_stop = ship._y + ship._length - 1  # высота низ вровень

            for y in range(sy_start, sy_stop + 1):  # от 0 к 9 вниз
                ship_matrix.append((sx_start, y))

        # смотрим пересечение
        for self_coords in self_matrix:
            for ship_coords in ship_matrix:
                if self_coords == ship_coords:
                    return True
        return False

    def is_out_pole(self, size=10):
        if self._tp == 1:  # horizont
            x_end = self._x + self._length - 1  # нашли существующий правый х
            if x_end <= size-1 and self._x >= 0:  # не выходит за поле по горизонтали
                return False
            else:
                return True

        if self._tp == 2:  # vertical
            y_down = self._y + self._length - 1  # нашли существующий нижний y
            if y_down <= size-1 and self._y >= 0:  # не выходит за поле по вертикали
                return False
            else:
                return True

    def __getitem__(self, item):
        return self._cells[item]

    def __setitem__(self, key, value):
        self._cells[key] = value







class GamePole:
    def __init__(self, size=10):
        self._size = size
        self._ships = []

    def init(self):
        self._ships = [Ship(4, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)),
                       Ship(3, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(2, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2)),
                       Ship(1, tp=randint(1, 2))]

        # self._ships = [Ship(4, tp=randint(1, 2))]

        # self._ships = [Ship(4, tp=1, x=0, y=0),
        #                Ship(3, tp=1, x=3, y=-4)]

        # self._ships = [Ship(4, tp=randint(1, 2)),
        #                Ship(3, tp=randint(1, 2)),
        #                Ship(3, tp=randint(1, 2))]

        # self._ships = [Ship(4, tp=1, x=0, y=0),
        #                Ship(3, tp=1, x=0, y=-2),
        #                Ship(2, tp=1, x=0, y=-4),
        #                Ship(1, tp=1, x=0, y=-6)]

        # self._ships = [Ship(4, tp=2, x=0, y=0),
        #                Ship(3, tp=2, x=2, y=0),
        #                Ship(2, tp=2, x=4, y=0),
        #                Ship(1, tp=2, x=6, y=0)]

        #расстановка случайным образом, чтобы не пересекались

        for ship in self._ships:
            flag = True
            while flag:
                x_e = self._size - 1
                y_d = self._size - 1

                x = randint(0, x_e)
                y = randint(0, y_d)

                #  зададим координаты кораблю
                ship.set_start_coords(x, y)
                # print(ship.__dict__, ship.get_start_coords())

                if ship._tp == 1:  # horizont



                    x_end = x + ship._length - 1
                    if x_end <= self._size-1:  # влезает по ширине (вертикаль проверять не надо)
                        # print(f'{ship.get_start_coords()} подходит по ширине')

                        tmp_ships = self._ships[:]
                        tmp_ships.remove(ship)  # все корабли без текущего
                        collide = 0  # число количества пересечений

                        for t_ship in tmp_ships:
                            if t_ship.__dict__['_x'] != None and t_ship.__dict__['_y'] != None:  # если у корабля заданы x,y
                                # проверка на пересечение
                                if ship.is_collide(t_ship):  # если пересечение есть
                                    collide += 1
                                else:  # если пересечений нет
                                    collide += 0
                            else:  # значит x=y=None, т.е. этот корабль не установлен, с ним нет пересечения
                                collide += 0

                        if collide == 0:  # ни одного пересечения
                            # print('годится')
                            flag = False  # выходим из цикла, рандом подошел
                        else:
                            flag = True  # повторный круг рандомов
                    else:
                        # print(f'{ship.get_start_coords()} не годится по ширине')
                        flag = True  # повторный круг рандомов


                if ship._tp == 2:  # vertical

                    y_down = y + ship._length - 1
                    if y_down <= self._size - 1:  #  влезает по высоте снизу (ширину не проверяем)
                        # print(f'{ship.get_start_coords()} подходит по высоте')

                        tmp_ships = self._ships[:]
                        tmp_ships.remove(ship)  # все корабли без текущего
                        collide = 0  # число количества пересечений

                        for t_ship in tmp_ships:
                            if t_ship.__dict__['_x'] != None and t_ship.__dict__['_y'] != None:  # если у корабля заданы x,y
                                # проверка на пересечение
                                if ship.is_collide(t_ship):  # если пересечение есть
                                    collide += 1
                                else:  # если пересечений нет
                                    collide += 0
                            else:  # значит x=y=None, т.е. этот корабль не установлен, с ним нет пересечения
                                collide += 0

                        if collide == 0:  # ни одного пересечения
                            # print('годится')
                            flag = False  # выходим из цикла, рандом подошел
                        else:
                            flag = True  # повторный круг рандомов
                    else:
                        # print(f'{ship.get_start_coords()} не годится по высоте')
                        flag = True  # повторный круг рандомов



    def get_ships(self):
        return self._ships





    def move_ships(self):
        ships = self.get_ships()  # существующая компановка кораблей

        for i in range(len(ships)):
            ship = ships[i]

            # получаем список, кортеж кортежей всех координат, занятых кораблями,
            # Все корабли без своего окружения. Без самого себя.
            other_ships_coords = self.ships_coords(ship)

            go = choice((-1, 1))  # выбери что-то одно

            if ship._tp == 1:  # horizont
                x_end = ship._x + ship._length - 1  # нашли существующий правый х
                tmp_ship = Ship(ship._length, ship._tp, ship._x, ship._y)  # создаем временный дубль выбранного корабля

                if go > 0:  # движение вправо
                    if x_end + go <= self._size-1:  # вписываюсь в правую границу поля
                        # новые координаты с окружением сдвинутого временного корабля
                        x_new = ship._x + go
                        y = ship._y
                        tmp_ship.set_start_coords(x_new, y)  # корабль в новом месте
                        new_ship_coord = self.full_ship_cords(tmp_ship)  # координаты с окружением корабля на новом месте

                        # если окружение координат нового места корабля никак не пересекается с голыми
                        # координатами всех кораблей за исключением его старого места, то можно двигать
                        if not set(new_ship_coord).intersection(set(other_ships_coords)):

                            ship.move(go)  # переместили НАПРАВО

                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships


                        else: # меняю направление
                            if ship._x - abs(go) >= 0:  # вписываюсь в левую границу поля

                                x_new = ship._x - abs(go)
                                y = ship._y
                                tmp_ship.set_start_coords(x_new, y)
                                new_ship_coord = self.full_ship_cords(tmp_ship)

                                if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                    ship.move(-go)  # переместили НАЛЕВО

                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships

                                else:
                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                    else:  # меняю направление
                        if ship._x - abs(go) >= 0:  # вписываюсь в левую границу поля

                            x_new = ship._x - abs(go)
                            y = ship._y
                            tmp_ship.set_start_coords(x_new, y)
                            new_ship_coord = self.full_ship_cords(tmp_ship)

                            if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                ship.move(-abs(go))  # переместили НАЛЕВО

                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                        else:
                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships

                elif go < 0: # движение влево
                    if ship._x - abs(go) >= 0:  # вписываюсь в левую границу поля

                        x_new = ship._x - abs(go)
                        y = ship._y
                        tmp_ship.set_start_coords(x_new, y)
                        new_ship_coord = self.full_ship_cords(tmp_ship)

                        if not set(new_ship_coord).intersection(set(other_ships_coords)):
                            ship.move(-abs(go))  # переместили НАЛЕВО

                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships

                        else: # меняю направление
                            if x_end + abs(go) <= self._size -1: # вписываюсь в правую границу поля

                                x_new = ship._x + abs(go)
                                y = ship._y
                                tmp_ship.set_start_coords(x_new, y)
                                new_ship_coord = self.full_ship_cords(tmp_ship)

                                if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                    ship.move(abs(go))  # переместили НАПРАВО

                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                                else:
                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                    else:  # меняю направление
                        if x_end + abs(go) <= self._size-1:  # вписываюсь в правую границу поля

                            x_new = ship._x + abs(go)
                            y = ship._y
                            tmp_ship.set_start_coords(x_new, y)
                            new_ship_coord = self.full_ship_cords(tmp_ship)

                            if not set(new_ship_coord).intersection(set(other_ships_coords)):

                                ship.move(abs(go))  # переместили НАПРАВО

                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                        else:
                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships


            if ship._tp == 2:  # vertical

                y_down = ship._y + ship._length - 1  # нашли существующий нижний y
                tmp_ship = Ship(ship._length,ship._tp, ship._x, ship._y)  # создаем временный дубль выбранного корабля

                if go > 0:  # движение ВНИЗ
                    if y_down + go <= self._size - 1:  # вписываюсь в НИЖНЮЮ границу поля

                        x = ship._x
                        y_new = ship._y + abs(go)
                        tmp_ship.set_start_coords(x, y_new)
                        new_ship_coord = self.full_ship_cords(tmp_ship)

                        if not set(new_ship_coord).intersection(set(other_ships_coords)):
                            ship.move(abs(go))  # переместили ВНИЗ

                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships

                        else:  # меняю направление
                            if ship._y - abs(go) >= 0:  # вписываюсь в ВЕРХНЮЮ границу
                                x = ship._x
                                y_new = ship._y - abs(go)
                                tmp_ship.set_start_coords(x, y_new)
                                new_ship_coord = self.full_ship_cords(tmp_ship)

                                if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                    ship.move(-abs(go))  # переместили ВНИЗ

                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                                else:
                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships

                    else:  # меняю направление
                        if ship._y - abs(go) >= 0:  # вписываюсь в ВЕРХНЮЮ границу

                            x = ship._x
                            y_new = ship._y - abs(go)
                            tmp_ship.set_start_coords(x, y_new)
                            new_ship_coord = self.full_ship_cords(tmp_ship)

                            if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                ship.move(-abs(go))  # переместили ВВЕРХ

                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                        else:
                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships

                elif go < 0:  # движение ВВЕРХ
                    if ship._y - abs(go) >= 0:  # вписываюсь в ВЕРХНЮЮ границу

                        x = ship._x
                        y_new = ship._y - abs(go)
                        tmp_ship.set_start_coords(x, y_new)
                        new_ship_coord = self.full_ship_cords(tmp_ship)

                        if not set(new_ship_coord).intersection(set(other_ships_coords)):
                            ship.move(-abs(go))  # переместили ВВЕРХ

                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships

                        else:  # меняю направление
                            if y_down + abs(go) <= self._size - 1:  # вписываюсь в НИЖНЮЮ границу
                                x = ship._x
                                y_new = ship._y + abs(go)
                                tmp_ship.set_start_coords(x, y_new)
                                new_ship_coord = self.full_ship_cords(tmp_ship)

                                if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                    ship.move(abs(go))  # переместили ВНИЗ

                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                                else:
                                    # здесь нужно перегрузить список объектов поля &&&
                                    self._ships.insert(i, ship)
                                    ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships

                    else:  # меняю направление
                        if y_down + abs(go) <= self._size - 1:  # вписываюсь в НИЖНЮЮ границу
                            x = ship._x
                            y_new = ship._y + abs(go)
                            tmp_ship.set_start_coords(x, y_new)
                            new_ship_coord = self.full_ship_cords(tmp_ship)

                            if not set(new_ship_coord).intersection(set(other_ships_coords)):
                                ship.move(abs(go))  # переместили ВНИЗ

                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                            else:
                                # здесь нужно перегрузить список объектов поля &&&
                                self._ships.insert(i, ship)
                                ships = self._ships
                        else:
                            # здесь нужно перегрузить список объектов поля &&&
                            self._ships.insert(i, ship)
                            ships = self._ships







    def show(self):
        matrix = self.get_pole()
        for line in matrix:
            print(*line)

    def get_pole(self):
        ships = self.get_ships()
        matrix = list()
        box = list()

        # создаем матрицу координат
        for y in range(0, self._size):  # от 0 к 9 (сверху вниз)
            for x in range(0, self._size):  # получили координату конкретной клетки
                box.append((x, y))
            matrix.append(box)
            box = list()

        # прорисовываем корабли
        for line in matrix:
            for point in line:  # проходимся по все координатам - точкам матрицы игрового поля

                for ship in ships:
                    # получим список кортежей координат для корабля
                    ship_matrix = []

                    if ship._tp == 1:  # horizont
                        sx_start = ship._x  # ширина влево вровень
                        sx_stop = ship._x + ship._length - 1  # ширина вправо вровень
                        sy_start = ship._y  # высота вровень

                        for x in range(sx_start, sx_stop + 1):
                            ship_matrix.append((x, sy_start))  # все клетки корабля слева-направо

                    if ship._tp == 2:  # vertical
                        sx_start = ship._x  # ширина вровень
                        sy_start = ship._y  # высота вверх вровень
                        sy_stop = ship._y + ship._length - 1 # высота низ вровень

                        for y in range(sy_start, sy_stop + 1):  # от 0 к 9 вниз
                            ship_matrix.append((sx_start, y))  # все клетки корабля сверху-вниз

                    # смотрим пересечение
                    for coords in ship_matrix:
                        if coords == point:  # часть корабля есть в точке, теперь нужно понять какая: 1 или подбитая
                            # кортежи координат корабля формируются друг за другом по х или у
                            i = ship_matrix.index(coords)  # получаем индекс совпавшего кортежа координат
                            ind = line.index(coords)
                            line.remove(coords)
                            line.insert(ind, ship._cells[i])  # тут 1 или попадание (переписываем координату на значение)


        # перегоним все в кортеж кортежей
        res = list()
        line = list()
        for l in matrix:
            for s in l:
                if type(s) == tuple:
                    line.append(0)  # если тут нет корабля, значит вода
                    # line.append('*')  # если тут нет корабля, значит вода
                else:
                    line.append(s)
            res.append(tuple(line))
            line = list()

        return tuple(res)


    def ships_coords(self, boat):  # список кортежей всех занятых координат от кораблей,
        # Все координаты без окружения
        # без самого себя
        ships = self.get_ships()
        ships.remove(boat)  # без себя
        matrix = list()

        for ship in ships:
            if ship._tp == 1:  # horizont
                x_start = ship._x
                x_stop = ship._x + ship._length - 1
                y_start = ship._y

                for x in range(x_start, x_stop + 1):
                    matrix.append((x, y_start))

            if ship._tp == 2:  # vertical
                x_start = ship._x
                y_start = ship._y
                y_stop = ship._y + ship._length - 1

                for y in range(y_start, y_stop + 1):  # от 0 к 9 вниз
                    matrix.append((x_start, y))

        return matrix


    def full_ship_cords(self, ship):
        # координаты корабля с его окружением
        res = list()
        if ship._tp == 1:  # horizont
            x_start = ship._x - 1  # шире на 1 влево
            x_stop = ship._x + ship._length  # шире на 1 вправо
            y_start = ship._y - 1  # выше на 1 вверх
            y_stop = ship._y + 1  # ниже на 1 вниз

            for y in range(y_start, y_stop + 1):  # от 0 к 9 вниз
                for x in range(x_start, x_stop + 1):
                    res.append((x, y))

        if ship._tp == 2:  # vertical
            x_start = ship._x - 1  # шире на 1 влево
            x_stop = ship._x + 1  # шире на 1 вправо
            y_start = ship._y - 1  # выше на 1 вверх
            y_stop = ship._y + ship._length  # ниже на 1 вниз

            for y in range(y_start, y_stop + 1):  # от 0 к 9 вниз
                for x in range(x_start, x_stop + 1):
                    res.append((x, y))
        return res






# SIZE_GAME_POLE = 10
#
# pole = GamePole(SIZE_GAME_POLE)
# pole.init()
#
# # for ship in pole._ships:
# #     print(ship.__dict__)
# # pole._ships[0]._cells = [4,'*', 4, 5]
#
# pole.show()
#
# pole.move_ships()
# print()
# pole.show()


# ship = Ship(2)
# ship = Ship(2, 1)
# ship = Ship(3, 2, 0, 0)
#
# assert ship._length == 3 and ship._tp == 2 and ship._x == 0 and ship._y == 0, "неверные значения атрибутов объекта класса Ship"
# assert ship._cells == [1, 1, 1], "неверный список _cells"
# assert ship._is_move, "неверное значение атрибута _is_move"
#
# ship.set_start_coords(1, 2)
# assert ship._x == 1 and ship._y == 2, "неверно отработал метод set_start_coords()"
# assert ship.get_start_coords() == (1, 2), "неверно отработал метод get_start_coords()"
#
# ship.move(1)
# s1 = Ship(4, 1, 0, 0)
# s2 = Ship(3, 2, 0, 0)
# s3 = Ship(3, 2, 0, 2)
#
# assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 0)"
# assert s1.is_collide(
#     s3) == False, "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 0, 2)"
#
# s2 = Ship(3, 2, 1, 1)
# assert s1.is_collide(s2), "неверно работает метод is_collide() для кораблей Ship(4, 1, 0, 0) и Ship(3, 2, 1, 1)"
#
# s2 = Ship(3, 1, 8, 1)
# assert s2.is_out_pole(10), "неверно работает метод is_out_pole() для корабля Ship(3, 1, 8, 1)"
#
# s2 = Ship(3, 2, 1, 5)
# assert s2.is_out_pole(10) == False, "неверно работает метод is_out_pole(10) для корабля Ship(3, 2, 1, 5)"
#
# s2[0] = 2
# assert s2[0] == 2, "неверно работает обращение ship[indx]"
#
# p = GamePole(10)
# p.init()
# for nn in range(5):
#     for s in p._ships:
#         assert s.is_out_pole(10) == False, "корабли выходят за пределы игрового поля"
#
#         for ship in p.get_ships():
#             if s != ship:
#                 assert s.is_collide(ship) == False, "корабли на игровом поле соприкасаются"
#     p.move_ships()
#
# gp = p.get_pole()
# assert type(gp) == tuple and type(gp[0]) == tuple, "метод get_pole должен возвращать двумерный кортеж"
# assert len(gp) == 10 and len(gp[0]) == 10, "неверные размеры игрового поля, которое вернул метод get_pole"
#
# pole_size_8 = GamePole(8)
# pole_size_8.init()





