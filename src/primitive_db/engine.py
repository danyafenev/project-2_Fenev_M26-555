import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import load_metadata, save_metadata


def welcome():
    print("Первая попытка запустить проект!")
    print()
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ")

        if command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        elif command == "exit":
            break
        else:
            print(f"Функции {command} нет. Попробуйте снова.")


def run():
    while True:
        metadata = load_metadata("db_meta.json")
        user_input = prompt.string("Введите команду: ")
        args = shlex.split(user_input)

        command = args[0]

        if command == "exit":
            break

        elif command == "help":
            print("create_table <имя> <столбец:тип> ...")
            print("list_tables")
            print("drop_table <имя>")
            print("exit")
            print("help")

        elif command == "create_table":
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata("db_meta.json", metadata)

        elif command == "drop_table":
            table_name = args[1]
            metadata = drop_table(metadata, table_name)
            save_metadata("db_meta.json", metadata)

        elif command == "list_tables":
            for table_name in metadata:
                print(table_name)

        else:
            print(f"Функции {command} нет. Попробуйте снова.")
