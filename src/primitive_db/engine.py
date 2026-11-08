import shlex

import prompt
from prettytable import PrettyTable

from primitive_db.core import (
    create_table,
    delete,
    drop_table,
    info,
    insert,
    select,
    update,
)
from primitive_db.parser import parse_values, parse_where
from primitive_db.utils import (
    create_cacher,
    load_metadata,
    load_table_data,
    save_metadata,
)


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
    
    cache_result, clear_cache = create_cacher()
    while True:
        metadata = load_metadata("db_meta.json")
        user_input = prompt.string("Введите команду: ")
        try:
            args = shlex.split(user_input)
        except ValueError:
            print("Ошибка ввода команды.")
            continue

        if not args:
            continue

        command = args[0]
        
        required_args = {
            "create_table": 3,
            "drop_table": 2,
            "insert": 4,
            "select": 3,
            "update": 6,
            "delete": 5,
            "info": 2,
        }

        if command in required_args and len(args) < required_args[command]:
            print("Недостаточно аргументов команды.")
            continue

        if command == "exit":
            break

        elif command == "help":
            print("create_table <имя> <столбец:тип> ...")
            print("drop_table <имя>")
            print("list_tables")
            print("info <имя>")
            print('insert into <таблица> values ("имя", 28, true)')
            print("select from <таблица> [where столбец = значение]")
            print("update <таблица> set столбец = значение where столбец = значение")
            print("delete from <таблица> where столбец = значение")
            print("help")
            print("exit")

        elif command == "create_table":
            table_name = args[1]
            columns = args[2:]
            metadata = create_table(metadata, table_name, columns)
            save_metadata("db_meta.json", metadata)
            clear_cache()

        elif command == "drop_table":
            table_name = args[1]
            result = drop_table(metadata, table_name)

            if result is not None:
                save_metadata("db_meta.json", result)
                clear_cache()

        elif command == "list_tables":
            for table_name in metadata:
                print(table_name)
        
        elif command == "insert":
            table_name = args[2]
            values_text = user_input.split("(", 1)[1].rsplit(")", 1)[0]
            values = parse_values(values_text)
            insert(metadata, table_name, values)
            clear_cache()

        
        elif command == "select":
            table_name = args[2]
            table_data = load_table_data(table_name)

            if "where" in args:
                where_text = user_input.split("where", 1)[1]
                where_clause = parse_where(where_text)
            else:
                where_clause = None

            key = (table_name, str(where_clause))
            result = cache_result(
                key,
                lambda: select(table_data, where_clause),
            )

            table = PrettyTable()
            table.field_names = [
                column.split(":")[0] for column in metadata[table_name]
            ]

            for row in result:
                table.add_row([row[column] for column in table.field_names])

            print(table)

        
        
        elif command == "update":
            table_name = args[1]

            set_text = user_input.split("set", 1)[1].split("where", 1)[0]
            where_text = user_input.split("where", 1)[1]

            set_clause = parse_where(set_text)
            where_clause = parse_where(where_text)

            update(metadata, table_name, set_clause, where_clause)
            clear_cache()

        
        elif command == "delete":
            table_name = args[2]
            where_text = user_input.split("where", 1)[1]
            where_clause = parse_where(where_text)

            delete(metadata, table_name, where_clause)
            clear_cache()

        elif command == "info":
            table_name = args[1]
            info(metadata, table_name)
        
        else:
            print(f"Функции {command} нет. Попробуйте снова.")
