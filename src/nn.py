from itertools import chain
import numpy as np


class DenseLayer:
    def __init__(self, n_inputs, n_neurons) -> None:
        self.weights = 0.1 * np.random.randn(n_inputs, n_neurons)
        self.biases = 0.1 * np.random.randn(1, n_neurons)
        # self.biases = np.zeros((1, n_neurons))
    
    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases

class ReLU:
    def forward(self, inputs):
        self.output = np.maximum(0, inputs)

class Softmax:
    def forward(self, inputs):
        exp_values = np.exp(inputs - np.max(inputs, axis=1, keepdims=True))
        probs = exp_values / np.sum(exp_values, axis=1, keepdims=True)
        self.output = probs


class NN:
    def __init__(self, inputs: list) -> None:
        self.inputs = np.array(inputs)
        self.possible_outputs = ["left", "right", "up", "down", "nothing"]

        # Input layer
        self.n_w1 = 3
        self.n_w2 = 5
        self.n_w3 = 5 # This will always be 5, bacuse of five outputs

        self.layer1 = DenseLayer(len(inputs), self.n_w1)
        self.activation1 = ReLU()

        # Middle layer
        self.layer2 = DenseLayer(self.n_w1, self.n_w2)
        self.activation2 = ReLU()

        # Output layer 
        self.layer3 = DenseLayer(self.n_w2, self.n_w3)
        self.activation3 = Softmax()

        weights = list(chain(*self.layer1.weights)) + list(chain(*self.layer2.weights)) + list(chain(*self.layer3.weights))
        biases = list(chain(*self.layer1.biases)) + list(chain(*self.layer2.biases)) + list(chain(*self.layer3.biases))
        self.genome = [weights, biases]

    def think(self):
        self.layer1.forward(self.inputs)
        self.activation1.forward(self.layer1.output)

        self.layer2.forward(self.activation1.output)
        self.activation2.forward(self.layer2.output)

        self.layer3.forward(self.activation2.output)
        self.activation3.forward(self.layer3.output)

        self.probs = self.activation3.output
        self.output = np.argmax(self.activation3.output)
        self.str_output = self.possible_outputs[self.output]

    def update_inputs(self, inputs: list):
        self.inputs = np.array(inputs)

if __name__ == "__main__":
    nn = NN([50, 50, 6])
    print(nn.layer1.biases)
    
    '''
    nn = NN([50, 100])
    nn.think()
    print(nn.str_output)

    nn.update_inputs([70, 10000])
    nn.think()
    print(nn.str_output)
    '''
