import argparse


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



def main():
    parse_args()
