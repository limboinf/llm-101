# today：2023-09-05 17:49
# by @python coding 小红书
from datetime import datetime


class C:

    __name: str = '@python coding'
    __star: float = 22.678

    def __format__(self, s) -> str:
        return (
            f'cc -> {s} '
            f'name: {C.__name} '
            f'star: {C.__star:.2f} '
        )

dt = datetime.now()

result = f'{C(): the day is {dt=:%Y-%m-%d}}'

print(result)


