from lasagne.layers import *
from lasagne.nonlinearities import linear
from lasagne.init import GlorotNormal
from network.network import Network
import theano.tensor as T

class NetworkImg(Network):
    def init_model(self, n_actions, observation_shape):
        self.observations=T.tensor4("X")
        nn = InputLayer((None,) + observation_shape, input_var=self.observations)
        conv1 = Conv2DLayer(nn, 8, 3, 1)
        #conv2 = Conv2DLayer(conv1, 32, 3, 1)
        nn1 = DenseLayer(conv1, 8)
        self.m = DenseLayer(nn1, n_actions, nonlinearity=linear)
        self.logsigma = DenseLayer(nn1, n_actions, nonlinearity=linear)
        self.model = [self.m, self.logsigma]
