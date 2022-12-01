"""Шаблон модуля my_sort"""
from typing import Optional, Callable


def get_leonardo_number(number: int) -> int:
    """
    Функция для вычисления числа Леонардо
    :param number: номер числа Леонардо, которое мы хотим получить
    :return: число Леонардо
    """

    # Первые два числа Леонарда равны 1, индексацию начинаем с нуля
    if number < 2:
        return 1

    # Иначе вычисляем число Леонардо по формуле:
    return get_leonardo_number(number - 1) + get_leonardo_number(number - 2) + 1


def my_sort(array: list, reverse: bool = False, key: Optional[Callable] = None,
            cmp: Optional[Callable] = None) -> list:
    # Куча будет храниться в виде списка деревьев Леонардо
    heap = []

    # Создание первоначальной кучи
    # Очередной элемент или объединяет две предыдущие кучи
    # или добавляет новую кучу из одного узла (дерево первого порядка)
    for index in range(len(array)):

        # Если у прошлых деревьев смежный порядок (например, 1 и 2,
        # 4 и 5, 8 и 9), то объединяем их в одно большое дерево;
        # Новая вершина - корень дерева.

        if len(heap) >= 2 and heap[-2] == heap[-1] + 1:
            heap.pop()
            heap[-1] += 1

        # Если первое условие не выполняется и порядок последнего
        # дерева равен 1, то добавляем дерево 0-го порядка.

        elif heap[-1] == 1:
            heap.append(0)

        # Иначе - добавляем дерево 1-го порядка.
        else:
            heap.append(1)



        restore_heap(lst, index, heap, leo_nums)
