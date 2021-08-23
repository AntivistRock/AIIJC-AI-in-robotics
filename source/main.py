import pybullet as pb
import time

import engine


class MySimulation (engine.Simulation):

    def _load(self):

        pb.setGravity(0, 0, -9.8)

        # ball

        ball_col_shape = pb.createCollisionShape(pb.GEOM_SPHERE, radius=0.2)
        ball_visual_shape = pb.createVisualShape(pb.GEOM_SPHERE, radius=0.2,
                                                 rgbaColor=[0.25, 0.75, 0.25, 1])

        pb_ball = pb.createMultiBody(1, ball_col_shape, ball_visual_shape, [0, 0, 3], [0, 0, 0, 1])

        # plane

        floor_col_shape = pb.createCollisionShape(pb.GEOM_PLANE)
        floor_visual_shape = pb.createVisualShape(pb.GEOM_BOX,
                                                  halfExtents=[10, 10, 0.0001], rgbaColor=[1, 1, .98, 1])

        pb_floor = pb.createMultiBody(0, floor_col_shape, floor_visual_shape, [0, 0, 0], [0, 0, 0, 1])

    def _update(self):
        pass


def main():

    env = engine.Environment()
    env.set_simulation(MySimulation())

    # for i in range(1000):
    #     env.update()
    #     time.sleep(1./100.)


if __name__ == "__main__":
    main()
