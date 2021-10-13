from .nn_model import SimpleRecurrentAgent
# from .teapot_detectron import TeapotDetectron

from torch import no_grad, Tensor, unsqueeze, load


class Model(object):

    def __init__(self, num_actions, num_channels=1):

        self.agent = SimpleRecurrentAgent(num_channels, num_actions).to('cuda')
        # self.detectron = TeapotDetectron()

    def forward(self, images, memory):
        self.agent.train()
        # image_with_mask = self.detectron.get_points(images)
        image_with_mask = unsqueeze(Tensor(images), 1).to('cuda')
        memory = (memory[0].to('cuda'), memory[1].to('cuda'))
        memory, output = self.agent(memory, image_with_mask)

        return memory, output
        pass

    def get_action(self, images, memory):
        self.agent.eval()
        with no_grad():
            # image_with_mask = self.detectron.get_points(images)
            image_with_mask = unsqueeze(unsqueeze(Tensor(images), 0), 0).to('cuda')
            memory = (memory[0].to('cuda'), memory[1].to('cuda'))
            memory, output = self.agent(memory, image_with_mask)
            output = (output[0].to('cpu'), output[1].to('cpu'))
            print(f"Вероятности: {output}")
            memory = (memory[0].to('cpu'), memory[1].to('cpu'))

            return memory, self.agent.sample_actions(output)

    def load_weights(self, PATH):
        self.agent.load_state_dict(load(PATH))
