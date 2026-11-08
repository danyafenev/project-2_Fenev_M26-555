from primitive_db.decorators import confirm_action, handle_db_errors, log_time
from primitive_db.utils import load_table_data, save_table_data


def create_table(metadata, table_name, columns):
    if table_name in metadata:
        print(f"Таблица {table_name} уже существует.")
        return metadata

    for column in columns:
        name, data_type = column.split(":")
        if data_type not in ("int", "str", "bool"):
            print(f"Некорректное значение: {data_type}. Попробуйте снова.")
            return metadata

    metadata[table_name] = ["ID:int"] + columns
    return metadata

@confirm_action("удаление таблицы")
def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует.")
        return metadata

    del metadata[table_name]
    return metadata

@handle_db_errors
@log_time
def insert(metadata, table_name, values):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует.")
        return

    columns = metadata[table_name][1:]

    if len(values) != len(columns):
        print("Некорректное количество значений.")
        return

    for column, value in zip(columns, values):
        name, data_type = column.split(":")

        if data_type == "int" and type(value) is not int:
            print(f"Некорректное значение: {value}.")
            return
        elif data_type == "str" and type(value) is not str:
            print(f"Некорректное значение: {value}.")
            return
        elif data_type == "bool" and type(value) is not bool:
            print(f"Некорректное значение: {value}.")
            return

    data = load_table_data(table_name)

    new_id = max((row["ID"] for row in data), default=0) + 1
    row = {"ID": new_id}

    for column, value in zip(columns, values):
        name = column.split(":")[0]
        row[name] = value

    data.append(row)
    save_table_data(table_name, data)

    return data

@handle_db_errors
@log_time
def select(table_data, where_clause=None):
    if where_clause is None:
        return table_data

    column, value = where_clause

    result = []
    for row in table_data:
        if row[column] == value:
            result.append(row)

    return result


@handle_db_errors
def update(metadata, table_name, set_clause, where_clause):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует.")
        return

    column, value = set_clause
    where_column, where_value = where_clause

    columns = {
        name: data_type
        for name, data_type in (
            item.split(":") for item in metadata[table_name]
        )
    }

    if column not in columns or where_column not in columns:
        print("Указанный столбец не существует.")
        return

    data_type = columns[column]

    if type(value).__name__ != data_type:
        print(f"Некорректный тип значения для столбца {column}.")
        return

    data = load_table_data(table_name)

    for row in data:
        if row[where_column] == where_value:
            row[column] = value

    save_table_data(table_name, data)
    return data


@handle_db_errors
@confirm_action("удаление записей")
def delete(metadata, table_name, where_clause):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует.")
        return

    data = load_table_data(table_name)
    column, value = where_clause

    data = [row for row in data if row[column] != value]

    save_table_data(table_name, data)
    return data


def info(metadata, table_name):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует.")
        return

    for column in metadata[table_name]:
        print(column)
