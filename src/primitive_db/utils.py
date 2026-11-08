import json
import os


def load_metadata(filepath):
    
    """Загружает метаданные базы данных из JSON-файла."""
    
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    
    """Сохраняет метаданные базы данных."""
    
    with open(filepath, "w") as file:
        json.dump(data, file)


def load_table_data(table_name):
    
    """Загружает записи таблицы."""
    
    try:
        with open(f"data/{table_name}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    
    """Сохраняет записи таблицы."""
    
    os.makedirs("data", exist_ok=True)

    with open(f"data/{table_name}.json", "w") as file:
        json.dump(data, file)


