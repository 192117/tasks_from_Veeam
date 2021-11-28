# Программа работает через библиотеку shutil и os.
# Запуск программы осуществляется из командной строки.
# Формат python путь_до_скрипта каталог-источник каталог-реплика время файл_для_логгирования
import time
import os
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
        file.write(value + "\n")


def delete_dir(path, filename):
    """Очистка каталога-реплики. Запись действий в логфайл с помощью функции write."""
    while os.listdir(path) != []:
        os.chdir(path)
        for file in os.listdir(path):
            if os.path.isdir(os.path.abspath(file)):
                try:
                    os.rmdir(file)
                    write(filename, "Delete directory: {}".format(file))
                    print("Delete directory: {}".format(file))
                except:
                    delete_dir(os.path.abspath(file))
            if os.path.isfile(os.path.abspath(file)):
                os.remove(file)
                write(filename, "Delete file: {}".format(file))
                print("Delete file: {}".format(file))


def copy_dir(path1, path2, filename):
    """
    Копирование файлов и подкаталогов из каталога-истоничка в каталог-реплику.
    Запись действий в логфайл с помощью функции write.
    """
    while len(os.listdir(path1)) != len(os.listdir(path2)):
        os.chdir(path1)
        for file in os.listdir(path1):
            if os.path.isfile(os.path.abspath(file)):
                shutil.copy2(os.path.abspath(file), path2)
                write(filename, "Copy file: {}".format(file))
                print("Copy file: {}".format(file))
            if os.path.isdir(os.path.abspath(file)):
                file_path, name = os.path.split(os.path.abspath(file))
                if os.path.isdir(os.path.join(path2, name)):
                    continue
                else:
                    os.mkdir(os.path.join(path2, name))
                    write(filename, "Create directory: {}".format(file))
                    print("Create directory: {}".format(file))
                    copy_dir(os.path.abspath(file), os.path.join(path2, name), filename)


def main():
    arguments = parser()
    if arguments.file1 and arguments.file2 and arguments.times and arguments.log:
        try:
            while True:
                delete_dir(arguments.file2, arguments.log)
                copy_dir(arguments.file1, arguments.file2, arguments.log)
                time.sleep(int(arguments.times))
        except Exception as err:
            print("Something's wrong!")
            print(err)
    else:
        print("Need more parameters.")


if __name__ == "__main__":
    main()