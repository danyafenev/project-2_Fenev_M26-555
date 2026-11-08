
## Управление таблицами

Команды:

- `create_table <имя_таблицы> <столбец1:тип> ...` — создать таблицу.
- `list_tables` — показать список таблиц.
- `drop_table <имя_таблицы>` — удалить таблицу.
- `help` — показать справку.
- `exit` — выйти из программы.

Поддерживаемые типы данных: `int`, `str`, `bool`.

### Пример использования

```text
Введите команду: create_table users name:str age:int
Введите команду: list_tables
users
Введите команду: drop_table users
Введите команду: list_tables
Введите команду: exit
```

## Демонстрация работы

[![Демонстрация работы базы данных](https://asciinema.org/a/MHtOPXKdjWPEEQgl.svg)](https://asciinema.org/a/MHtOPXKdjWPEEQgl)


## Работа с данными

Добавление записи:

```text
insert into users values ("Daniil", 29, true)
```

Просмотр всех записей:

```text
select from users
```

Поиск записей по условию:

```text
select from users where age = 29
```

Изменение записи:

```text
update users set age = 29 where name = "Daniil"
```

Удаление записи:

```text
delete from users where ID = 1
```

Просмотр структуры таблицы:

```text
info users
```

## Дополнительные возможности

- Обработка ошибок с помощью декоратора `handle_db_errors`.
- Подтверждение удаления таблиц и записей через `confirm_action`.
- Замер времени выполнения операций `insert` и `select`.
- Кеширование повторных запросов `select`.
- Автоматическая очистка кеша после изменения данных.
- Вывод результатов запросов в виде таблиц с помощью PrettyTable.