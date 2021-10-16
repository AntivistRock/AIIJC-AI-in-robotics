from .nn_model import SimpleRecurrentAgent
# from .teapot_detectron import TeapotDetectron

from torch import no_grad, Tensor, unsqueeze


class Model(object):

    def __init__(self, num_actions, num_channels=1):
        pass

        self.agent = SimpleRecurrentAgent(num_channels, num_actions)
        # self.detectron = TeapotDetectron()

    def forward(self, images, memory):
        # image_with_mask = self.detectron.get_points(images)
        image_with_mask = unsqueeze(unsqueeze(Tensor(images), 0), 0)
        memory, output = self.agent(memory, image_with_mask)

        return memory, output
        pass

    def get_action(self, images, memory):
        self.agent.eval()
        with no_grad():
            # image_with_mask = self.detectron.get_points(images)
            image_with_mask = unsqueeze(unsqueeze(Tensor(images), 0), 0)
            print("IM WITH MSK shape:", image_with_mask.shape)
            memory, output = self.agent(memory, image_with_mask)

            return memory, self.agent.sample_actions(output)
