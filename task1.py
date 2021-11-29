# Программа написана под Windows.
# Запуск python процессов.
import time
import psutil
import os
import subprocess
import csv


def write_start(filename):
    """
    Создание csv файла данных и запись шапки файла. Файл будет располагаться в директории данного скрипта
    с именем процесса, который будет запущен в нём.
    """
    with open(os.path.join(os.getcwd(), filename + '.csv'), "a") as file:
        file_writer = csv.writer(file, delimiter = ";", lineterminator="\r")
        file_writer.writerow(["cpu", "WorkingSet", "PrivateBytes", "handle"])

def write(filename, value):
    """
    Запись в csv файл данных.
    """
    with open(os.path.join(os.getcwd(), filename + '.csv'), "a") as file:
        file_writer = csv.writer(file, delimiter = ";", lineterminator="\r")
        file_writer.writerow(value)

def main():
    """
    Основная функция, которая проверяет наличие двух параметров и запускается. Если их нет, то распечатает сообщение.
    Если что-то не получится, то выведет также сообщение.
    """
    file = input("Write path: ")
    times = input("Write time: ")
    if file and times:
        try:
            filename = file.split("\\")[-1].split(".")[0]
            write_start(filename)
            new_process = subprocess.Popen(['python', file]) # Запуск python процесса.
            new_process_pid = new_process.pid
            for proc_from_all in psutil.process_iter():
                if proc_from_all.pid == new_process_pid:
                    while True:
                        result = [str(proc_from_all.cpu_percent()), str(proc_from_all.memory_info()[0]),
                                  str(proc_from_all.memory_info()[-1]), str(proc_from_all.num_handles())]
                        write(filename, result)
                        time.sleep(int(times))
        except Exception as err:
            print("Something's wrong")
            print(err)
    else:
        print('Need 2 parameters!')


if __name__ == "__main__":
    main()