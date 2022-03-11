import numpy as np


class NeuralNetwork(object):
    '''Creates a fully connected/dense neural network with 2 hidden layers'''

    def __init__(self, numInput, numHidden1, numHidden2, numOutput):
        '''Initializes the neural network'''
        self.biasNode = 1                                # bias node variable set to 1 for node count calculations & readability
        # Add bias node for first hidden layer
        self.numInput = numInput + self.biasNode
        # Adds bias node for second hidden layer
        self.numHidden1 = numHidden1 + self.biasNode
        self.numHidden2 = numHidden2
        self.numOutput = numOutput

        self.w_i_h1 = np.random.randn(
            self.numHidden1-self.biasNode, self.numInput)
        self.w_h1_h2 = np.random.randn(self.numHidden2, self.numHidden1)
        self.w_h2_o = np.random.randn(self.numOutput, self.numHidden2)

        self.ReLU = lambda x: max(0, x)

    def softmax(self, x):
        '''Returns elements from last layer of network as a probability distribution which adds up to 1'''
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    def feedForward(self, inputs):
        '''Takes the inputs & weights and processes the softmax output of the neural network'''
        inputsBias = inputs[:]                  # copies input array
        # adds bias value for hidden layer 1
        inputsBias.append(1)

        h1 = np.dot(self.w_i_h1, inputsBias)    # feed input to hidden layer 1
        h1 = [self.ReLU(x) for x in h1]         # activates hidden layer 1

        # add bias value for hidden layer 2
        h1.append(1)

        # feed hidden layer 1 to hidden layer 2
        h2 = np.dot(self.w_h1_h2, h1)
        h2 = [self.ReLU(x) for x in h2]         # activate hidden layer 2

        output = np.dot(self.w_h2_o, h2)        # feed to output layer
        output = self.softmax(output)
        return output

    def getWeightsLinear(self):
        '''Returns the current weights set in the network'''
        flat_w_i_h1 = list(self.w_i_h1.flatten())
        flat_w_h1_h2 = list(self.w_h1_h2.flatten())
        flat_w_h2_o = list(self.w_h2_o.flatten())
        return(flat_w_i_h1 + flat_w_h1_h2 + flat_w_h2_o)

    def setWeightsLinear(self, genome):
        '''Sets the weights for the network'''

        numWeights_I_H1 = (self.numHidden1-self.biasNode) * self.numInput
        numWeights_H1_H2 = (self.numHidden2) * self.numHidden1

        self.w_i_h1 = np.array(genome[:numWeights_I_H1])
        self.w_i_h1 = self.w_i_h1.reshape(
            (self.numHidden1-self.biasNode, self.numInput))

        self.w_h1_h2 = np.array(
            genome[numWeights_I_H1:(numWeights_H1_H2+numWeights_I_H1)])
        self.w_h1_h2 = self.w_h1_h2.reshape((self.numHidden2, self.numHidden1))

        self.w_h2_o = np.array(genome[(numWeights_H1_H2+numWeights_I_H1):])
        self.w_h2_o = self.w_h2_o.reshape((self.numOutput, self.numHidden2))


def generate_neural_net(algorithm):
    input_node_counts = {"a": 8, "b": 10, "c": 16,
                         "d": 18, "e": 12, "f": 14, "g": 24, "h": 26}
    numInputNodes = input_node_counts[algorithm]

    numHiddenNodes1, numHiddenNodes2, numOutputNodes = 8, 8, 4
    network = NeuralNetwork(numInputNodes, numHiddenNodes1,
                            numHiddenNodes2, numOutputNodes)
    # Calculates the size of the individual using input, output and hidden layer neuron counts (accounting for bias nodes for hidden layers)
    ind_size = ((numInputNodes+1) * numHiddenNodes1) + ((numHiddenNodes1+1)
                                                        * numHiddenNodes2) + (numHiddenNodes2 * numOutputNodes)
    return ind_size, network
