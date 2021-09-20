import threading as mt
from multiprocessing import cpu_count


class ThreadPool(object):
    def __init__(self, function, n_parallel=cpu_count()):
        self._function = function
        self._n_parallel = n_parallel

    def get_n_parallel(self):
        return self._n_parallel

    def run(self, quantity, arguments=None, enable_warnings=False):

        if enable_warnings:
            if quantity % self._n_parallel != 0:
                raise RuntimeWarning(f"{self.run.__name__} => Quantity don't divisible by n_parallels")

            if arguments and len(arguments) != quantity:
                raise AttributeError(f"{self.run.__name__} => Len of arguments must be equal quantity")

        quantity_alone = quantity // self._n_parallel

        threads = [
            self._Thread(
                quantity_alone, self._function, arguments[i * quantity_alone: (i + 1) * quantity_alone]
            ) for i in range(self._n_parallel)
        ]

        [thread.start() for thread in threads]
        [thread.join() for thread in threads]

        return [(*thread.reply,)[0] for thread in threads]

    class _Thread(mt.Thread):
        def __init__(self, quantity, function, arguments):
            mt.Thread.__init__(self)

            self._quantity = quantity
            self._function = function
            self._arguments = arguments

            self.reply = []

        def run(self):
            self.reply = [
                self._function(*self._arguments[i])
                for i in range(self._quantity)
            ]
