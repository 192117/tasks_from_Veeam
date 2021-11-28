# Программа работает через библиотеку shutil
# Запуск программы осуществляется из командной строки.
# Формат python путь_до_скрипта каталог-источник каталог-реплика время файл_для_логгирования
import time
import argparse
import shutil

def parser():
    """
    Парсинг командной строки: после имени file1 указывается путь до каталога-источника,
    после имени file1 указывается путь до каталога-реплики, после имени time интервал синхронизации,
    после имени log указываеть путь до файла логирования.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file1')
    parser.add_argument('file2')
    parser.add_argument('times')
    parser.add_argument('log')
    return parser.parse_args()

def write(filename, value):
    """
    Запись в файл данных.
    """
    with open(filename, "a") as file:
        file.write(value)

def main():
    arguments = parser()
    if arguments.file1 and arguments.file2 and arguments.times and arguments.log:
        try:
            while True:
                shutil.rmtree(arguments.file2)
                write(arguments.log, "Удалена вся директория {}\n".format(arguments.file2))
                print("Удалена вся директория {}\n".format(arguments.file2))
                shutil.copytree(arguments.file1, arguments.file2)
                write(arguments.log, "Скопировано всё содержимое {} в {}\n".format(arguments.file1, arguments.file2))
                print("Скопировано всё содержимое {} в {}\n".format(arguments.file1, arguments.file2))
                time.sleep(int(arguments.times))
        except Exception as err:
            print("Something's wrong!")
            print(err)
    else:
        print("Need more parameters.")

if __name__ == "__main__":
    main()