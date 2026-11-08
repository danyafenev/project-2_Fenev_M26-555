import time
from functools import wraps


def handle_db_errors(func):
    
    """Обрабатывает ошибки при работе с базой данных."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, TypeError, FileNotFoundError) as error:
            print(f"Ошибка базы данных: {error}")

    return wrapper


def confirm_action(action_name):
    
    """Запрашивает подтверждение перед выполнением действия."""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            answer = input(
                f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: '
            )

            if answer != "y":
                print("Операция отменена.")
                return

            return func(*args, **kwargs)

        return wrapper

    return decorator


def log_time(func):
    
    """Выводит время выполнения функции."""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = func(*args, **kwargs)
        elapsed = time.monotonic() - start

        print(f"Функция {func.__name__} выполнилась за {elapsed:.3f} секунд.")
        return result

    return wrapper

def create_cacher():
    
    """Создаёт замыкание для кеширования результатов."""
    
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