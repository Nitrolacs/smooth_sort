import argparse
import textwrap
import os

import pygame as pg

from typing import Union
from random import shuffle

from PIL import Image


class CreatorGifImages:
    def __init__(self, directory="gif"):
        self.directory = directory
        self.frames = []
        self.frames_count = 0
        self.gif_number = 1

        self.path = self.create_path(directory)

    def create_path(self, directory):
        if os.path.exists(directory):
            self.directory = directory
        path = f"{self.directory}\\gif{self.gif_number}.gif"
        while os.path.exists(path):
            self.gif_number += 1
            path = f"{self.directory}\\gif{self.gif_number}.gif"
        return path


def reading_file(file_name: str = "") -> Union[str, bool]:
    """Чтение строки из файла"""
    file_strings = ""
    string = ""

    if not os.path.exists(file_name):
        print("Такого файла не существует.")
        return False

    with open(file_name, "r", encoding='utf-8') as file:
        for line in file:
            file_strings += line

    if file_strings and file_strings != " " * len(file_strings):
        string = ''.join(file_strings.split("\n"))

    print("Считано из файла: ")

    for line in textwrap.wrap(string, width=120)[:10]:
        print(line)

    string = file_strings.replace('\n', '')
    return string


def add_frame_to_gif(data, width: int, height: int, gif):
    image = Image.frombytes("RGBA", (width, height), data)
    gif.frames_count += 1
    gif.frames.append(image)


def visualize_array(array: list, heap_size: int, length: int, width: int,
                    height: int, min_value: int, max_value: int,
                    screen: pg.Surface, gif):
    norm_x = width / length
    norm_w = norm_x if norm_x > 1 else 1
    h_caf = (height - 100) / (max_value - min_value)

    for index, value in enumerate(array):
        norm_h = abs(value) * h_caf

        h_caf = (height - 100) / (max_value - min_value)
        norm_min = min_value * h_caf
        zero_h = height - 1 + norm_min

        if value > 0:
            norm_y = height - norm_h - (height - zero_h)
        else:
            norm_y = zero_h

        if index != heap_size:
            cur_color = (185, 185, 185)
        else:
            cur_color = (255, 0, 0)

        pg.draw.rect(screen, (255, 255, 255), (
            norm_x * index, 0, norm_w, height))
        pg.draw.rect(screen, cur_color, (norm_x * index, norm_y,
                                         norm_w, norm_h))

        if value > 0:
            sqrt_y = norm_y - norm_w
        else:
            sqrt_y = norm_y + norm_h - norm_w

        pg.draw.rect(screen, (0, 0, 0),
                     (norm_x * index, sqrt_y, norm_w, norm_w))

        pg.draw.line(screen, (255, 255, 255),
                     (0, zero_h), (width, zero_h), 2)
        pg.display.update()

    if gif:
        add_frame_to_gif(pg.image.tostring(screen, "RGBA"), width, height,
                         gif)

    pg.time.wait(50)


def create_gif(gif):
    """
    Метод сохранения гифки в директорию
    """
    print("Please, wait, started gif creation")
    gif.frames[0].save(gif.path, save_all=True,
                       append_images=gif.frames[1:],
                       optimize=True,
                       duration=100,
                       loop=0)
    print(f"Gif was successfully saved in {gif.directory} directory")
    gif.frames[0].close()
    gif.frames.clear()
    gif.frames_count = 0
    gif.gif_number += 1


def sort_visualization(array: list, reverse: bool, make_gif: bool,
                       visualize: bool) -> list:
    """
    Функция отрисовки процесса сортировки
    :param visualize:
    :param make_gif: Нужно ли делать gif-изображение
    :param array: Массив с данными для сортировки
    :param reverse: Порядок сортировки
    :return: None
    """

    width = height = length = min_value = max_value = 0
    screen = None
    gif = None

    if visualize:
        pg.init()
        width, height = 800, 600
        min_value, max_value = min(array), max(array)
        length = len(array)

        if make_gif:
            gif = CreatorGifImages()

        # Инициализирует окно
        screen = pg.display.set_mode((width, height))
        pg.display.set_caption("SmoothSort")
        bg_color = (255, 255, 255)
        screen.fill(bg_color)

    # Куча будет храниться в виде списка деревьев Леонардо
    heap = []

    key = lambda x: x
    cmp = lambda x, y: x < y

    def _get_leonardo_number(number: int) -> int:
        """
        Функция для вычисления числа Леонардо
        :param number: номер числа Леонардо, которое мы хотим получить
        :return: число Леонардо
        """

        # Первые два числа Леонарда равны 1, индексацию начинаем с нуля
        if number < 2:
            return 1

        # Иначе вычисляем число Леонардо по формуле:
        return _get_leonardo_number(number - 1) + _get_leonardo_number(
            number - 2) + 1

    def _add_new_root() -> None:
        """
        Обновляет список размера деревьев Леонардо в лесу после того, как
        новый узел был добавлен.
        :return: None
        """

        # Если лес пустой, то добавляем дерево 1 порядка.

        if not heap:
            heap.append(1)

        # Если у прошлых деревьев смежный порядок (например, 1 и 2,
        # 4 и 5, 8 и 9), то объединяем их в одно большое дерево;
        # Новая вершина - корень дерева.

        elif len(heap) >= 2 and heap[-2] == heap[-1] + 1:
            heap.pop()
            heap[-1] += 1

        # Если первое условие не выполняется и порядок последнего
        # дерева равен 1, то добавляем дерево 0-го порядка.

        elif heap[-1] == 1:
            heap.append(0)

        # Иначе - добавляем дерево 1-го порядка.
        else:
            heap.append(1)

    def _create_heap() -> None:

        # Создание первоначальной кучи
        # Очередной элемент или объединяет две предыдущие кучи
        # или добавляет новую кучу из одного узла (дерево первого порядка)
        for heap_end in range(len(array)):
            # Обновляем порядки деревьев
            _add_new_root()

            # Меняем местами корневые узлы деревьев.
            # Возвращает [индекс кучи, индекс размера]
            new_index, size_index = _fix_roots(heap_end, len(heap) - 1)

            # "Исправляет" дерево путем просейки.
            _sift_down(new_index, heap[size_index])

    def _fix_roots(start_heap_index: int,
                   start_size_index: int) -> (int, int):
        """
        Изменяет 'кучу' на месте, предполагая существование кучи Леонардо
        с деревьями, имеющими размеры в порядке,
        заданном параметром 'sizes'
        :param start_heap_index:
        :param start_size_index:
        :return:
        """

        # Переменные в этой функции ссылаются на индексы
        cur = start_heap_index
        size_cur = start_size_index

        # Продолжаем 'исправлять' корни, пока мы не окажемся у самого левого
        # корня
        while size_cur > 0:
            next_element = cur - _get_leonardo_number(heap[size_cur])
            # Прерываем цикл, если следующий корень строго
            # не больше текущего корня
            if cmp(key(array[next_element]), key(array[cur])) != reverse:
                break

            # Прерываем цикл, если следующий корень не больше, чем оба дочерних
            # элемента текущего корня и если размер текущего дерева не равен 0
            # или 1

            if heap[size_cur] > 1:
                right = cur - 1
                left = right - _get_leonardo_number(heap[size_cur] - 2)
                if cmp(key(array[next_element]),
                       key(array[right])) != reverse or \
                        cmp(key(array[next_element]),
                            key(array[left])) != reverse:
                    break

            # Меняем места текущий корень со следующим корнем
            temp = array[cur]
            array[cur] = array[next_element]
            array[next_element] = temp

            # Продолжаем, начиная со следующего узла как с текущего
            size_cur = size_cur - 1
            cur = next_element

        return cur, size_cur

    def _sift_down(root_index: int, tree_size: int) -> None:
        """
        "Исправляет" дерево размера tree_size с корнем root_index в куче
        :param root_index: индекс корня
        :param tree_size: размер дерева
        :return: None
        """
        cur = root_index
        # Продолжаем итерацию, пока не останется дочерних узлов
        while tree_size > 1:
            right = cur - 1
            left = cur - 1 - _get_leonardo_number(tree_size - 2)

            if visualize:
                visualize_array(array, cur, length, width, height,
                                min_value,
                                max_value, screen, gif)

            # Корень не меньше размера обоих потомков
            if cmp(key(array[left]), key(array[cur])) != reverse and \
                    cmp(key(array[right]), key(array[cur])) != reverse:
                break
            # Правый дочерний элемент не меньше левого дочернего
            elif cmp(key(array[left]), key(array[right])) != reverse:
                array[cur], array[right] = array[right], array[cur]
                cur = right
                tree_size = tree_size - 2
            # Левый потомок самый большой из трёх
            else:
                array[cur], array[left] = array[left], array[cur]
                cur = left
                tree_size = tree_size - 1

    def _dequeue_max(heap_sz: int) -> None:
        """
        Удаляет максимумы.
        :param heap_sz: размер кучи.
        :return:
        """
        removed_size = heap.pop()
        # Если самое правое дерево имеет один узел
        if removed_size == 0 or removed_size == 1:
            pass  # Уже удалено
        # Если у самого правого дерева двое детей
        else:
            # Добавляем порядки обратно
            heap.append(removed_size - 1)
            heap.append(removed_size - 2)
            # Вычисляем индексы левого и правого потомка
            left_idx = heap_sz - _get_leonardo_number(heap[-1]) - 1
            right_idx = heap_sz - 1
            left_size_idx = len(heap) - 2
            right_size_idx = len(heap) - 1
            # "Исправляем левого потомка"
            idx, size_idx = _fix_roots(left_idx, left_size_idx)
            _sift_down(idx, heap[size_idx])
            # "Исправляем правого потомка"
            idx, size_idx = _fix_roots(right_idx,
                                       right_size_idx)
            _sift_down(idx, heap[size_idx])

    _create_heap()
    for heap_size in range(len(array) - 1, -1, -1):

        if visualize:
            visualize_array(array, heap_size, length, width, height, min_value,
                            max_value, screen, gif)

        _dequeue_max(heap_size)

    running_visualization = True
    while running_visualization:
        pg.display.update()

        for event in pg.event.get():

            if event.type == pg.QUIT:
                pg.quit()
                running_visualization = False

    if make_gif:
        create_gif(gif)

    return array


def parse_args() -> bool:
    """Обработка параметров командной строки"""
    # Осуществляем разбор аргументов командной строки
    parser = argparse.ArgumentParser(description="Плавная сортировка")

    # Метод add_mutually_exclusive_group() создает взаимоисключающую группу
    # параметров командной строки
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-s", "--strings", dest="strings", nargs='+', type=str,
                       help="Список строк через пробел")
    group.add_argument("-d", "--digits", dest="digits", nargs='+', type=int,
                       help="Список чисел через пробел")
    group.add_argument("-f", "--file", type=str, dest="file",
                       help="Путь до файла")
    group.add_argument("-rd", "--randomized_digits", dest="rand_dig", type=int,
                       help="Количество чисел, которое"
                            " необходимо сгенерировать")

    parser.add_argument("-r", "--reverse", dest="reverse", action="store_true",
                        help="Порядок сортировки")
    parser.add_argument("-v", "--visualize", action="store_true",
                        dest="visualize",
                        help="Нужно ли визуализировать сортировку?")
    parser.add_argument("-g", "--gif", dest="gif", action="store_true",
                        help="Нужно ли сохранить гифку с визуализацией "
                             "процесса сортировки?")

    # В эту переменную попадает результат разбора аргументов командной строки.
    args = parser.parse_args()

    array = []
    # Проверяем аргументы командной строки

    if args.strings:
        array = args.strings

    elif args.digits:
        array = args.digits

    elif args.file:
        result = reading_file(args.file)
        if result:
            try:
                array = [int(number) for number in result.split()]
            except ValueError:
                array = result.split()
        else:
            return False

    elif args.rand_dig:
        if args.rand_dig > 0:
            array = [number for number in
                     range(-(args.rand_dig // 2), args.rand_dig // 2)]

            # Функция shuffle перемешивает изменяемую последовательность
            # случайным образом
            shuffle(array)

    sorted_array = sort_visualization(array, args.reverse, args.gif,
                                      args.visualize)

    print("Результат:")
    print(sorted_array)


def main():
    parse_args()


if __name__ == "__main__":
    main()
