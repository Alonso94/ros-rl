from lasagne.layers import *
from lasagne.nonlinearities import linear
from lasagne.init import GlorotNormal
from network.network import Network

class NetworkImg(Network):
    def init_model(self, n_actions, observation_shape):

