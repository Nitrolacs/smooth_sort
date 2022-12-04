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
    """
    Плавная сортировка.
    :param array: сортируемый список
    :param reverse: флаг, определяющий вариант сортировки.
                    False - по неубыванию
                    True - по невозрастанию
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

    def create_heap() -> None:

        # Создание первоначальной кучи
        # Очередной элемент или объединяет две предыдущие кучи
        # или добавляет новую кучу из одного узла (дерево первого порядка)
        for heap_end in range(len(array)):

            # Если у прошлых деревьев смежный порядок (например, 1 и 2,
            # 4 и 5, 8 и 9), то объединяем их в одно большое дерево;
            # Новая вершина - корень дерева.

            if not heap:
                heap.append(1)

            elif len(heap) >= 2 and heap[-2] == heap[-1] + 1:
                heap.pop()
                heap[-1] += 1

            # Если первое условие не выполняется и порядок последнего
            # дерева равен 1, то добавляем дерево 0-го порядка.

            else:
                if heap[-1] == 1:
                    heap.append(0)

                # Иначе - добавляем дерево 1-го порядка.
                else:
                    heap.append(1)

            new_index, size_index = fix_roots(heap_end, len(heap) - 1)
            sift_down(new_index, heap[size_index])

    """
    # updates the list of sizes of leonardo trees in a forest after a new node is
    # added
    def _add_new_root(size_list):
        # case 1: Empty forest. Add L_1 tree.
        if len(size_list) == 0:
            size_list.append(1)
        # case 2: Forest with two rightmost trees differing in size by 1.
        #         Replace the last two trees of size L_k-1 and L_k-2 by a single
        #         tree of size L_k.
        elif len(size_list) > 1 and size_list[-2] == size_list[-1] + 1:
            size_list[-2] = size_list[-2] + 1
            del size_list[-1]
        # case 3: Add a new tree, either L_1 or L_0
        else:
            # case 1: Rightmost tree is an L_1 tree. Add L_0 tree.
            if size_list[-1] == 1:
                size_list.append(0)
            # case 2: Rightmost tree is not an L_1 tree. Add L_1 tree.
            else:
                size_list.append(1)
    """

    def fix_roots(start_heap_index: int,
                  start_size_index: int):
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

            # stop if the next root is not greater than both children of the
            # current root, if those children exist, i.e. the size of the
            # current tree is not 0 or 1.

            if heap[size_cur] > 1:
                right = cur - 1
                left = right - get_leonardo_number(heap[size_cur] - 2)
                if cmp(key(array[next_element]),
                       key(array[right])) != reverse or \
                        cmp(key(array[next_element]),
                            key(array[left])) != reverse:
                    break

            # swap the current root with the next root
            temp = array[cur]
            array[cur] = array[next_element]
            array[next_element] = temp
            # continue, starting with the next root as the current root
            size_cur = size_cur - 1
            cur = next_element

        return cur, size_cur

    # Fixes the tree of size tree_size rooted at root_idx in heap, where heap is otherwise a valid heap
    def sift_down(root_index, tree_size):
        cur = root_index
        # continue iterating until there are no child nodes
        while tree_size > 1:
            right = cur - 1
            left = cur - 1 - get_leonardo_number(tree_size - 2)
            # the root is at least as large as both children
            if cmp(key(array[left]), key(array[cur])) != reverse and \
                    cmp(key(array[right]), key(array[cur])) != reverse:
                break
            # the right child is at least as large as the left child
            elif cmp(key(array[left]), key(array[right])) != reverse:
                array[cur], array[right] = array[right], array[cur]
                cur = right
                tree_size = tree_size - 2
            # the left child is the greatest of the three
            else:
                array[cur], array[left] = array[left], array[cur]
                cur = left
                tree_size = tree_size - 1

    # removes the max value from the graph
    def _dequeue_max(heap_size):
        removed_size = heap.pop()
        # case 1: rightmost tree has a single node
        if removed_size == 0 or removed_size == 1:
            pass  # already removed
        # case 2: rightmost tree has two children
        else:
            # add sizes back
            heap.append(removed_size - 1)
            heap.append(removed_size - 2)
            # calculate indices of left and right children
            left_idx = heap_size - get_leonardo_number(heap[-1]) - 1
            right_idx = heap_size - 1
            left_size_idx = len(heap) - 2
            right_size_idx = len(heap) - 1
            # fix left child
            idx, size_idx = fix_roots(left_idx, left_size_idx)
            sift_down(idx, heap[size_idx])
            # fix right child
            idx, size_idx = fix_roots(right_idx,
                                       right_size_idx)
            sift_down(idx, heap[size_idx])

    create_heap()
    for heap_size in range(len(array) - 1, -1, -1):
        _dequeue_max(heap_size)

    return array
