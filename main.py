# Создать декоратор для использования кэша. Т.е. сохранять аргументы и результаты в словарь, если вызывается функция
# с агрументами, которые уже записаны в кэше - вернуть результат из кэша, если нет - выполнить функцию.
# Кэш лучше хранить в json.
import json
from typing import Callable


def json_logging(func: Callable):
    try:
        with open(f'{func.__name__}.json', 'r') as data:
            result_list = json.load(data)
    except FileNotFoundError:
        result_list = []

    def wrapper(*args, **kwargs):
        dict_temp: dict
        for dict_temp in result_list:
            key = tuple(dict_temp.get("args"))
            if key == args or key == kwargs:
                return dict_temp

        result = func(*args, **kwargs)
        result_list.append({'args': args,
                            **kwargs,
                            'result': result})
        with open(f'{func.__name__}.json', 'w') as data:
            json.dump(result_list, data, indent=4)
        return result

    return wrapper


@json_logging
def sum_args(*args: tuple) -> int:
    return sum(args)


@json_logging
def show(**kwargs: dict) -> None:
    for k, v in kwargs.items():
        print(f"{k} - {v}")


if __name__ == '__main__':
    sum_args(34, 12, 6, 112)
    show(Seether='Broken (feat EmyLi)',
         Poets_of_the_Fall='Late Goodbye',
         And_one='Military Fashion Show',
         Keane='Everybody\'s Changing')
