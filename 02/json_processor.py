import json
from typing import Callable


def process_json(
        json_str: str,
        required_keys: list[str] | None = None,
        tokens: list[str] | None = None,
        callback: Callable[[str, str], None] | None = None,
) -> None:
    data = json.loads(json_str)

    # Если не заданы ключи, берем все ключи из json строки
    if not required_keys:
        required_keys = list(data.keys())

    # Если не заданы токены, выходим
    if not tokens:
        return

    for key, value in data.items():
        # Проверка вхождения ключа в словарь
        if key in required_keys:
            for token in tokens:
                # Проверка вхождения токена (без учета регистра)
                if token.lower() in value.lower():
                    if callback:
                        callback(key, token)
