<<<<<<< Updated upstream
import pybullet as pb
import pybullet_data
=======
from decorators import add_timer
from engine import Environment, EnvThreadPool
from my_simulation import MySimulation

>>>>>>> Stashed changes

@add_timer
def test_1():
    env = Environment(simulation=MySimulation())
    for i in range(10):
        env.run()

<<<<<<< Updated upstream
from source import engine


class MySimulation(engine.res.Simulation):

    def _load(self):
        pb.setGravity(0, 0, -9.8)

        pb.setAdditionalSearchPath(pybullet_data.getDataPath())
        pb.loadURDF("plane.urdf")

        vm_data = engine.ViewMatrix.ViewMatrixData([0, 0, 5], 10, 2)
        pm_data = engine.ProjMatrix.ProjMatrixData(0.01, 20)

        self.camera = engine.Camera(200, 200, vm_data, pm_data)

    def _update(self):
        plt.imshow(self.camera.snapshot())


def main():
    env = engine.Environment()
    env.set_simulation(MySimulation())

    for i in range(10000):
        env.update()
=======

@add_timer
def test_2():
    env_pool = EnvThreadPool(lambda: MySimulation(), 10)
    env_pool.interact()


def main():
    test_1()
    test_2()
>>>>>>> Stashed changes


if __name__ == "__main__":
    main()
