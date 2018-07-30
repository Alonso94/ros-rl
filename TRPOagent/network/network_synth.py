from lasagne.layers import *
from lasagne.nonlinearities import linear
from lasagne.init import GlorotNormal
from network.network import Network

class NetworkSynth(Network):
    def init_model(self, n_actions, observation_shape):
        nn = InputLayer((None,) + observation_shape, input_var=self.observations)
        nn1 = DenseLayer(nn, 256, W=GlorotNormal())
        nn2 = DenseLayer(nn1, 64, W=GlorotNormal())
        self.m = DenseLayer(nn2, n_actions, nonlinearity=linear)
        self.logsigma = DenseLayer(nn2, n_actions, nonlinearity=linear)
        self.model = [self.m, self.logsigma]
