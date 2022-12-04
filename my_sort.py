"""
Модуль плавной сортировки
"""

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
    """
    Плавная сортировка.
    :param array: сортируемый список
    :param reverse: флаг, определяющий вариант сортировки.
                    False - по не убыванию
                    True - по не возрастанию
    :param key: функция, вычисляющая значение, на основе которого будет
                производится сортировка. Должна принимать один аргумент и
                возвращать значение.
    :param cmp: функция сравнения, должна принимать два аргумента и возвращать
                значение.
    :return: новый список с отсортированными элементами.
    """

    key = key if key else lambda x: x
    cmp = cmp if cmp else lambda x, y: x < y

    # Куча будет храниться в виде списка деревьев Леонардо
    heap = []

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
            next_element = cur - get_leonardo_number(heap[size_cur])
            # Прерываем цикл, если следующий корень строго
            # не больше текущего корня
            if cmp(key(array[next_element]), key(array[cur])) != reverse:
                break

            # Прерываем цикл, если следующий корень не больше, чем оба дочерних
            # элемента текущего корня и если размер текущего дерева не равен 0
            # или 1

            if heap[size_cur] > 1:
                right = cur - 1
                left = right - get_leonardo_number(heap[size_cur] - 2)
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
            left = cur - 1 - get_leonardo_number(tree_size - 2)
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
            left_idx = heap_sz - get_leonardo_number(heap[-1]) - 1
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
        _dequeue_max(heap_size)

    return array
