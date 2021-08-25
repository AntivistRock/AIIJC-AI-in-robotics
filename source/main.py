import pybullet as pb

from source import engine, models


class MySimulation(engine.res.Simulation):

    kettle = models.KettleLoader()
    robot = models.RobotLoader()

    def _load(self):
        pb.setGravity(0, 0, -9.8)

        self.kettle.load()
        self.robot.load()

    def _upload(self):
        self.kettle.upload()
        self.robot.upload()

    def _update(self):
        pass


def main():

    env = engine.Environment()
    env.set_simulation(MySimulation())

    for i in range(10000):
        env.update()


if __name__ == "__main__":
    main()
