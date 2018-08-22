from itertools import count
from collections import OrderedDict
from util import *
import numpy as np
from gazeboplanner.gadapter.gazebo_tools import TurtleBot


class TRPOAgent(TurtleBot):

    def __init__(self, env):
        self.env = env
        self.n_actions = self.env.act_shape
        self.observation_shape = self.env.obs_shape
        self.init_network()

    def act(self, obs, sample=True):
        raise NotImplementedError

    def init_network(self):
        raise NotImplementedError


    def train_path(self, max_kl=0.01, cg_damping=0.1, numeptotal=0, max_pathlength=500, n_timesteps=30000):
        print("Rollout")
        paths = self.rollout(max_pathlength, n_timesteps)
        print("Made rollout")

        # Updating policy.
        observations = np.concatenate([path["observations"] for path in paths])
        actions = np.concatenate([path["actions"] for path in paths])
        returns = np.concatenate([path["cumulative_returns"] for path in paths])
        old_m = np.concatenate([path["m"] for path in paths])
        old_logstd = np.concatenate([path["logstd"] for path in paths])
        inputs_batch = [observations, actions, returns, old_m, old_logstd]

        old_weights = self.net.get_flat_weights()

        def fisher_vector_product(p):
            """gets intermediate grads (p) and computes fisher*vector """
            return self.net.compute_fisher_vector_product(observations, p) + cg_damping * p

        flat_grad = self.net.get_surrogate_gradients(*inputs_batch)

        stepdir = conjugate_gradient(fisher_vector_product, -flat_grad)
        shs = .5 * stepdir.dot(fisher_vector_product(stepdir))
        lm = np.sqrt(shs / max_kl)
        fullstep = stepdir / lm

        # Compute new weights with linesearch in the direction we found with CG

        def losses_f(flat_weights):
            self.net.load_flat_weights(flat_weights)
            return self.net.compute_losses(*inputs_batch)

        new_weights = linesearch(losses_f, old_weights, fullstep, max_kl)

        self.net.load_flat_weights(new_weights)

        # Report current progress
        L_surr, kl, entropy = self.net.compute_losses(*inputs_batch)
        episode_rewards = np.array([path["rewards"].sum() for path in paths])

        stats = OrderedDict()
        numeptotal += len(episode_rewards)
        stats["Total number of episodes"] = numeptotal
        stats["Average sum of rewards per episode"] = episode_rewards.mean()
        stats["Std of rewards per episode"] = episode_rewards.std()
        stats["Entropy"] = entropy
        stats["KL between old and new distribution"] = kl
        stats["Surrogate loss"] = L_surr
        return stats, episode_rewards

    def learn(self, reward=530,  max_pathlength=500, n_timesteps=30000):
        rewards = []
        for i in count(1):
            print("\n********** Iteration %i ************" % i)
            stats, episode_rewards = self.train_path(max_pathlength=max_pathlength, n_timesteps=n_timesteps)
            if episode_rewards.mean() > reward:
                break
            rewards.append(episode_rewards.mean())
            for k, v in stats.items():
                print(k + ": " + " " * (40 - len(k)) + str(v))
            i += 1
        return rewards, i

    def rollout(self, max_pathlength=2500, n_timesteps=50000):
        raise NotImplementedError

    def play(self, env):
        obs = env.reset()
        done = False
        reward = 0
        l = 0
        while done is not True:
            a = self.act(obs, sample=False)[0]
            for i in range(self.n_actions):
                obs, r, done = env.step([i, a[i]])
                if done:
                    break
            reward += r
            l += 1
            print(l, ')', r, obs, a)

    def grasp(self, env):
        raise NotImplementedError

    def pickup(self, env, act_form, prev_direct, table_radius):
        raise NotImplementedError

    def putdown(self, env, act_form, prev_direct, table_radius):
        raise NotImplementedError
