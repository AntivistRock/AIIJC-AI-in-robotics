from decorators import add_timer
from engine import Environment, EnvThreadPool
from my_simulation import MySimulation


@add_timer
def test_1():
    env = Environment(simulation=MySimulation())
    for i in range(10):
        env.run()


@add_timer
def test_2():
    env_pool = EnvThreadPool(lambda: MySimulation(), 10)
    env_pool.interact()


def main():
    test_1()
    test_2()


if __name__ == "__main__":
    main()
