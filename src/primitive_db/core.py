
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


def drop_table(metadata, table_name):
    if table_name not in metadata:
        print(f"Таблица {table_name} не существует.")
        return metadata

    del metadata[table_name]
    return metadata
