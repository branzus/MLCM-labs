import random
import numpy as np
import pprint


class Layer:


    def __init__(self, n_input, n_neurons, activation_function=None, weights=None):
        random.seed()
        self.weights = weights if weights is not None else [[random.random() for i in range(n_neurons)] for i in range(n_input)]
        self.activation_function = activation_function

        self.activation = None
        self.error = None
        self.delta = None


    def activate(self, x):
        s = np.dot(x, self.weights)
        self.activation = self.compute_activation(s)
        return self.activation


    def compute_activation(self, s):

        if self.activation_function is None:
            return s

        
        if self.activation_function == 'sigmoid':
            return 1 / (1 + np.exp(-s))
        
        return s

    def compute_activation_derivative(self, s):

        if self.activation_function is None:
            return s

        if self.activation_function == 'sigmoid':
            return s * (1 - s)

        return s


    def __repr__(self):
        return str(self.weights)



class NeuralNetwork:

    def __init__(self):
        self.layers = []

    def add_layer(self, layer):

        self.layers.append(layer)


    def feed_forward(self, x):

        for layer in self.layers:
            x = layer.activate(x)
        return x

    def predict(self, x):
        return np.argmax(self.feed_forward(x), axis=1)


    def backpropagate(self, x, y, l_rate):

        out = self.feed_forward(x)

        for i in reversed(range(len(self.layers))):
            layer = self.layers[i]
            
            if layer == self.layers[-1]:
                layer.error = y - out
                layer.delta = layer.error * layer.compute_activation_derivative(out)
            else:
                layer.error = np.dot(self.layers[i+1].weights, self.layers[i+1].delta)
                layer.delta = layer.error * layer.compute_activation_derivative(layer.activation)



        for i in range(len(self.layers)):
            layer = self.layers[i]
            inp = np.atleast_2d(x if i == 0 else self.layers[i-1].activation)
            layer.weights += layer.delta * inp.T * l_rate



    def train(self, x, y, l_rate, epochs, mse_k=10):

        mse_lst = []
        
        for i in range(epochs):
            for j in range(len(x)):
                self.backpropagate(x[j], y[j], l_rate)
            if i % mse_k == 0:
                mse = np.mean(np.square(y -  nn.feed_forward(x)))
                mse_lst.append(mse)
                print('Epoch {0}, Error: {1}'.format(i, mse))

        return mse_lst

if __name__ == "__main__":

    nn = NeuralNetwork()
    nn.add_layer(Layer(6,2, 'sigmoid'))
    nn.add_layer(Layer(2,2, 'sigmoid'))
    
    
    x = [[1,1,0,0,0,0],
         [1,0,1,0,0,0],
         [1,0,0,1,0,0],
         [1,0,0,0,1,0],
         [1,0,0,0,0,1],
         [0,1,1,0,0,0],
         [0,1,0,1,0,0],
         [0,1,0,0,1,0],
         [0,1,0,0,0,1],
         [0,0,1,1,0,0],
         [0,0,1,0,1,0],
         [0,0,1,0,0,1],
         [0,0,0,1,1,0],
         [0,0,0,1,0,1],
         [0,0,0,0,1,1]]
    y = [[0,1],
         [0,1],
         [1,0],
         [1,0],
         [1,0],
         [0,1],
         [1,0],
         [1,0],
         [1,0],
         [1,0],
         [1,0],
         [1,0],
         [0,1],
         [0,1],
         [0,1]]
       
    errors = nn.train(x, y, 0.3, 1000, 30)

    print (nn.predict(x))
    print (nn.feed_forward(x))    
    
    
