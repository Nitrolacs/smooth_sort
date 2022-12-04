import argparse
import textwrap
import os

from typing import Union
from random import shuffle

import my_sort


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


def parse_args():
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

    elif args.random:
        if args.random > 0:
            array = [number for number in range(1, args.random + 1)]

            # Функция shuffle перемешивает изменяемую последовательность
            # случайным образом
            shuffle(array)

    sorted_array = my_sort.my_sort(array, args.reverse)

    print("Результат:")
    print(sorted_array)


def main():
    parse_args()


if __name__ == "__main__":
    main()
