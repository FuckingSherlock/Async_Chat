import inspect
import logging
from datetime import date

frame = inspect.stack()[-1]
# print(str(*a).split('\\')[12])
module = inspect.getmodule(frame[0])
filename_with_ex = module.__file__.split('\\')[-1]
filename = filename_with_ex.split('.')[0]

logger = logging.getLogger('app.func')
formatter = logging.Formatter("%(asctime)s %(levelname)s %(module)s %(message)s")
fh = logging.FileHandler(f'{str(date.today())}_{filename}.log', encoding='utf-8')
# fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


def func_log(func):
    def wrapper(*args, **kwargs):
        code_obj_name = inspect.currentframe().f_back.f_code.co_name
        func_args = inspect.signature(func).bind(*args, **kwargs).arguments
        func_args_str = ", ".join(map("{0[0]} = {0[1]!r}".format, func_args.items()))
        if code_obj_name == '<module>':
            logger.debug(
                f"Функция {func.__qualname__}({func_args_str}) вызвана из файла {filename_with_ex}")
        else:
            logger.debug(
                f"Функция {func.__qualname__}({func_args_str}) вызвана из функции {code_obj_name}")
        return func(*args, **kwargs)
    return wrapper


# if __name__ == '__main__':
    # console = logging.StreamHandler()
    # console.setLevel(logging.DEBUG)
    # console.setFormatter(formatter)
    # logger.addHandler(console)
    # logger.info('Тестовый запуск логирования')
