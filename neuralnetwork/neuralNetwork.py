import numpy as np
from neuralnetwork.utils import sigmoid, tanh, stepFunction

class NeuralNetwork:
    def __init__(self, input_nodes, hidden_nodes=0, output_nodes=0, learning_rate=0.1, activation=sigmoid):
        if type(input_nodes) == NeuralNetwork:
            neural = input_nodes
            self.input_nodes = neural.input_nodes
            self.hidden_nodes = neural.hidden_nodes
            self.output_nodes = neural.output_nodes

            self.weights_inputToHidden = np.copy(neural.weights_inputToHidden)
            self.weights_hiddenToOutput = np.copy(neural.weights_hiddenToOutput)

            self.hidden_bias = np.copy(neural.hidden_bias)
            self.output_bias = np.copy(neural.output_bias)
        else:
            self.input_nodes = input_nodes
            self.hidden_nodes = hidden_nodes
            self.output_nodes = output_nodes

            self.weights_inputToHidden = np.random.uniform(low=-1, high=1, size=(self.hidden_nodes, self.input_nodes))
            self.weights_hiddenToOutput = np.random.uniform(low=-1, high=1, size=(self.output_nodes, self.hidden_nodes))

            self.hidden_bias = np.random.uniform(low=-1, high=1, size=(self.hidden_nodes, 1))
            self.output_bias = np.random.uniform(low=-1, high=1, size=(self.output_nodes, 1))

        self.learning_rate = learning_rate
        self.activation = activation

    def Predict(self, input_array):
        # generate the hidden outputs
        inputs = np.reshape(input_array, (len(input_array), 1))
        hidden = np.matmul(self.weights_inputToHidden, inputs)
        hidden += self.hidden_bias
        # pass it through the activation function
        hidden = self.activation.func(hidden)

        # generate the output's output
        output = np.matmul(self.weights_hiddenToOutput, hidden)
        output += self.output_bias
        # pass it through the activation function
        output = self.activation.func(output)
        # return in an array format matrix(nDimensionalArray) --to--> flat array
        return output.flatten()

    def Train(self, input_array, label_array, debug=False):
        # ---- FEED FORWARD -----
        
        # generate the hidden outputs
        inputs = np.reshape(input_array, (len(input_array), 1))
        hidden = np.matmul(self.weights_inputToHidden, inputs)
        hidden += self.hidden_bias
            # pass it through the activation function
        hidden = self.activation.func(hidden)

        # generate the output's output
        outputs = np.matmul(self.weights_hiddenToOutput, hidden)
        outputs += self.output_bias
           # pass it through the activation function
        outputs = self.activation.func(outputs) # prediction

        #convert array -> matrix  # correct output
        targets = np.reshape( label_array, (len(label_array), 1) )

        #calculate the error wkt: ERROR = CORRECT_OUTPUT - PREDICTION
        output_errors = targets - outputs


        # ----- BACKPROPAGATION -------


        # calculate gradient
        # gradient = outputs * ( 1 - outputs)
        gradients = self.activation.dfunc(outputs)
        gradients *= output_errors
        gradients *= self.learning_rate

        # calculate the change in weights . deltas
        transpose_hidden = hidden.T
        weight_hiddenOutput_deltas = np.matmul(gradients, transpose_hidden)

        # adjust weights by deltas  and the bias by its deltas(gradients)
        self.weights_hiddenToOutput += weight_hiddenOutput_deltas
        self.output_bias += gradients

        # calculate the hiddent layer errors
        transpose_weights_hiddenToOutput = self.weights_hiddenToOutput.T
        hidden_errors = np.matmul(transpose_weights_hiddenToOutput, output_errors)
        # calculate hidden gradient
        hidden_gradients = self.activation.dfunc(hidden)
        hidden_gradients *= hidden_errors
        hidden_gradients *= self.learning_rate

        # calculate deltas
        transpose_inputs = inputs.T
        weight_inputHidden_deltas = np.matmul(hidden_gradients, transpose_inputs)
        #adjust weight and bias
        self.weights_inputToHidden += weight_inputHidden_deltas
        self.hidden_bias += hidden_gradients

        if debug==True:
            print("outputs = {}".format(outputs))
            print("targets = {}".format(targets))

    def mutate(self, func):
        self.weights_inputToHidden = func(self.weights_inputToHidden)
        self.weights_hiddenToOutput = func(self.weights_hiddenToOutput)
        self.hidden_bias = func(self.hidden_bias)
        self.output_bias = func(self.output_bias)

    def setLearningRate(self, learning_rate=0.1):
        self.learning_rate = learning_rate



    def setActivationFunction(self, func=sigmoid):
        self.activation = func

    def copy(self):
        return NeuralNetwork(self)

    def __repr__(self):
        return f' id:{id(self)}, inputs:{self.input_nodes}, output_nodes:{self.output_nodes} '
