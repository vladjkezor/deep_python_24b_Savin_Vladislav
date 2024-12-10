cpdef loads(str json_string):
    cdef dict result = {}
    cdef str key

    if not (json_string.startswith('{') and json_string.endswith('}')):
        raise TypeError("Invalid JSON")

    json_string = json_string[1:-1].strip()

    for item in json_string.split(','):
        key, value = item.split(':', 1)
        key = key.strip()
        value = value.strip()

        if not (key.startswith('"') and key.endswith('"')):
            raise TypeError('Invalid JSON key format')
        key = key[1:-1]

        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        elif value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except:
                raise TypeError('Unsupported JSON value format')

        result[key] = value

    return result


cpdef dumps(dict dict_inst):
    cdef list json_items = []
    cdef str key

    if not isinstance(dict_inst, dict):
        raise TypeError('Input must be a dict')

    for key, value in dict_inst.items():
        if not isinstance(key, str):
            raise TypeError('Key must be a string')
        if isinstance(value, str):
            value = f'"{value}"'
        elif not isinstance(value, (int, float)):
            raise TypeError('Unsupported value type')

        json_items.append(f'"{key}": {value}')

    return '{' + ', '.join(json_items) + '}'


