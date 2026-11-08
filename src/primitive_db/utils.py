import json


def load_metadata(filepath):
    try:
        with open(filepath, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath, data):
    with open(filepath, "w") as file:
        json.dump(data, file)


def load_table_data(table_name):
    try:
        with open(f"data/{table_name}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name, data):
    with open(f"data/{table_name}.json", "w") as file:
        json.dump(data, file)



def create_cacher():
    cache = {}

    def cache_result(key, value_func):
        if key in cache:
            return cache[key]

        result = value_func()
        cache[key] = result
        return result

    def clear_cache():
        cache.clear()

    return cache_result, clear_cache

