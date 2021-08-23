import pybullet as pb

from source import engine


class MySimulation(engine.res.Simulation):

    def _load(self):
        pb.setGravity(0, 0, -9.8)

    def _update(self):
        pass


def main():

    env = engine.Environment()
    env.set_simulation(MySimulation())

    for i in range(10000):
        env.update()


if __name__ == "__main__":
    main()
