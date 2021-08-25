from time import sleep

import pybullet as pb
import pybullet_data

from matplotlib import pyplot as plt

from source import engine, models


class MySimulation(engine.res.Simulation):
    kettle = models.Kettle()
    robot = models.Robot()

    def _load(self):
        pb.setGravity(0, 0, -9.8)
        pb.setRealTimeSimulation(1)

        self.kettle.load()
        self.robot.load()
        
        pb.setAdditionalSearchPath(pybullet_data.getDataPath())
        pb.loadURDF("plane.urdf")

        vm_data = engine.ViewMatrixData([0, 0, 0.5], 2, 2, (0, -10, 0))
        pm_data = engine.ProjMatrixData(0.01, 20)

        self.camera = engine.Camera(320, 200, vm_data, pm_data)

    def _upload(self):
        self.kettle.upload()
        self.robot.upload()

    def _update(self):

        plt.imshow(self.camera.snapshot())

        sleep(1)


def main():
    env = engine.Environment(pb.GUI)
    env.set_simulation(MySimulation())

    while True:
        env.update()


if __name__ == "__main__":
    main()
