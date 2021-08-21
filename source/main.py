import pybullet as pb
import pybullet_data

import time


def main():
    phys_client = pb.connect(pb.GUI)
    pb.setAdditionalSearchPath(pybullet_data.getDataPath())

    pb.loadURDF("plane.urdf")

    for i in range(10000):
        pb.stepSimulation()
        time.sleep(1./240.)

    pb.disconnect(phys_client)


if __name__ == "__main__":
    main()
