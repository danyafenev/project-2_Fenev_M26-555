def parse_values(text):
    values = []

    for value in text.split(","):
        value = value.strip()

        if value.lower() == "true":
            values.append(True)
        elif value.lower() == "false":
            values.append(False)
        elif value.startswith('"') and value.endswith('"'):
            values.append(value[1:-1])
        else:
            values.append(int(value))

    return values

def parse_where(text):
    column, value = text.split("=", 1)
    column = column.strip()
    value = parse_values(value)[0]

    return column, value