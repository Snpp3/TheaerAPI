import os


def create_folder_if_doesnt_exist(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)


def check_input(data, schema):
    invalid_input = []
    for arg in schema:
        if schema[arg] == int:
            if not is_int(data[arg]):
                invalid_input.append({
                    f'{arg}': f'Incorrect type. Expecting: {schema[arg]}, Actual: {type(data[arg])}'
                })
        elif type(schema[arg]) == list:
            if not isinstance(data[arg], list):
                invalid_input.append({
                    f'{arg}': f'Incorrect type. Expecting: {list}, Actual: {type(data[arg])}'
                })
                continue
            expected_type = schema[arg][0]
            for value in data[arg]:
                if not isinstance(value, expected_type):
                    invalid_input.append({
                        f'{value}': f'Incorrect type. Expecting: {expected_type}, Actual: {type(value)}'
                    })
        elif not isinstance(data[arg], schema[arg]):
            invalid_input.append({
                f'{arg}': f'Incorrect type. Expecting: {schema[arg]}, Actual: {type(data[arg])}'
            })

    return invalid_input if len(invalid_input) != 0 else None


def is_int(candidate):
    try:
        int(candidate)
        return True
    except Exception:
        return False
