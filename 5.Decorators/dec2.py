from datetime import datetime

def logger_2(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            start_time = datetime.now().strftime('Дата: %d.%m.%y | Время: %H:%M:%S')
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as file:
                file.write(f'{start_time}\n{old_function}\n{args}{kwargs}\n{result}\n\n')

            return old_function(*args, **kwargs)

        return new_function

    return __logger
