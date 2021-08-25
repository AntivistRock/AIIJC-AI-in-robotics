import threading
import pybullet as pb
from psutil import cpu_count

from . import Environment


class EnvThreadPool(object):

    def __init__(self, simulation_creator, games_count=100, n_parallel_games=cpu_count()):
        self.environments = [Environment(pb.DIRECT) for _ in range(n_parallel_games)]
        [env.set_simulation(simulation_creator()) for env in self.environments]

        self.threads = []
        games_alone = games_count // n_parallel_games

        if games_count % n_parallel_games == 0:
            [self.threads.append(self.EnvThread(
                env, games_alone
            )) for env in self.environments]
        else:
            for i in range(n_parallel_games - 1):
                self.threads.append(self.EnvThread(
                    self.environments[i], games_alone
                ))
            self.threads.append(self.EnvThread(
                self.environments[-1], games_count % n_parallel_games
            ))

    def interact(self):

        for thread in self.threads:
            thread.start()

        for thread in self.threads:
            thread.join()

        return [thread.history for thread in self.threads]

    class EnvThread(threading.Thread):
        def __init__(self, environment, games_count):
            threading.Thread.__init__(self)
            self.environment = environment
            self.games_count = games_count
            self.history = []

        def run(self):
            for i in range(self.games_count):
                self.history.append(self.environment.run())
