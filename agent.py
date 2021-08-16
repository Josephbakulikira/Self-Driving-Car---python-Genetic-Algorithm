from car import Car
from neuralnetwork.neuralNetwork import NeuralNetwork
from neuralnetwork.utils import tanh

class Agent(Car):
    def __init__(self, x, y, angle):
        super(Agent, self).__init__(x, y, angle)
        self.inputs = 7
        self.brain = NeuralNetwork(self.inputs, 10, 2)
        self.brain.activation = tanh
        self.max_lifeSpan = 2000
        self.max_idle = 50

    def Update(screen, dt, trackLines, debug):
        self.update(screen, dt, trackLines, debug)
        # output = self.brain.Predict(self.)
        print(output)
