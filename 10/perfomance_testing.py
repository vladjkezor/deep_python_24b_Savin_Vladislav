import json
from time import time

import custom_json
from faker import Faker


def create_json(n_elements):
    fake = Faker()
    data = "{"
    for i in range(n_elements - 1):
        data += f'"key{i + 1}": ' + (
            f'"{fake.first_name()}", '
            if i % 2 == 0
            else f"{fake.random_number()}, "
        )
    return data + f'"key{n_elements}": ' + str(float(42)) + "}"


def test_performance(n_elements):
    print(f"Number of elements = {n_elements}")
    data = create_json(n_elements)
    t0 = time()
    original_loads_res = json.loads(data)
    print(f"json.loads time --- {time() - t0}")

    t0 = time()
    custom_loads_res = custom_json.loads(data)
    print(f"custom_json.loads time --- {time() - t0}")
    print(
        f"json_loads_res == custom_json_loads_res == "
        f"{original_loads_res == custom_loads_res}"
    )
    print()

    t0 = time()
    original_dumps_res = json.dumps(original_loads_res)
    print(f"json.dumps time --- {time() - t0}")

    t0 = time()
    custom_dumps_res = custom_json.dumps(original_loads_res)
    print(f"custom_json.dumps time --- {time() - t0}")
    print(
        f"json_dumps_res == custom_json_dumps_res == "
        f"{original_dumps_res == custom_dumps_res}"
    )


if __name__ == "__main__":
    N_ELEMENTS = 1000000
    test_performance(N_ELEMENTS)
