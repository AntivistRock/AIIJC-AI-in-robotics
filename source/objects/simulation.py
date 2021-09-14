from time import sleep

import pybullet as pb
import pybullet_data

import engine
import objects


class Simulation(engine.res.Simulation):

    def __init__(self, pb_client):
        engine.res.Simulation.__init__(self, pb_client)

        self.robot = objects.Robot(self.pb_client)

    def _load(self):
        # self.pb_client.setGravity(0, 0, -9.8)
        self.pb_client.setAdditionalSearchPath(pybullet_data.getDataPath())
        self.pb_client.setRealTimeSimulation(1)

        self.plane = self.pb_client.loadURDF("plane.urdf")
        self.robot.load()

        vm_data = engine.ViewMatrixData()
        pm_data = engine.ProjMatrixData(0.01, 20)

        self.camera = engine.Camera(320, 200, vm_data, pm_data)

    def _upload(self):
        self.robot.upload()

    def _update(self):

        state = self.pb_client.getLinkState(self.robot.arm, self.robot.end_effector_link_index)

        pos = list(state[0])
        ang = list(self.pb_client.getEulerFromQuaternion(state[1]))

        pos = engine.rotate(pos, [0.1, 0.1, 0])

        self.camera.update_view_matrix([
            engine.ViewMatrixData.SetCameraPos(pos),
            engine.ViewMatrixData.SetEulerAngles(ang),
        ])

        arm_target_pos = self.pb_client.calculateInverseKinematics(
            self.robot.arm, self.robot.end_effector_link_index, pos)

        self.pb_client.setJointMotorControlArray(
            self.robot.arm, self.robot.joint_indices,
            pb.POSITION_CONTROL, targetPositions=arm_target_pos
        )

        self.camera.snapshot()

        sleep(1)

        return True

    def get_history(self):
        pass
