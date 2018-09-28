from util import *
import numpy as np
from network.network_img import NetworkImg
import cv2
import rospy
from agent.agent_TRPO import TRPOAgent


class AgentImg(TRPOAgent):
    def act(self, obs, sample=True):
        m = self.net.get_mean([obs])[0]
        log_std = self.net.get_logstd([obs])[0]
        rnd = np.random.normal(size=self.n_actions)
        if sample:
            action = np.exp(log_std) * rnd + m
        else:
            action = m
        return action, m, log_std

    def init_network(self):
        self.net = NetworkImg(self.n_actions, self.observation_shape)

    def rollout(self, max_pathlength=2500, n_timesteps=50000):
        paths = []
        total_timesteps = 0
        self.env.state = np.zeros(4)
        while total_timesteps < n_timesteps:
            observations, actions, rewards, action_m, action_logstd = [], [], [], [], []
            observation = self.proc_img(self.env.reset())
            if total_timesteps % 4 == 0:
                self.env.state = np.zeros(4)
            done = False
            for _ in range(max_pathlength):
                action, m, logstd = self.act(observation)
                observations.append(observation)
                actions.append(action)
                action_m.append(m)
                action_logstd.append(logstd)
                reward = 0
                for i in range(self.n_actions):
                    observation, r, done = self.env.step([i, action[i]])
                    observation = self.proc_img(observation)
                    reward += r
                rewards.append(reward)
                total_timesteps += 1
                if done or total_timesteps % max_pathlength == 0:
                    path = {"observations": np.array(observations),
                            "m": np.array(action_m),
                            "logstd": np.array(action_logstd),
                            "actions": np.array(actions),
                            "rewards": np.array(rewards),
                            "cumulative_returns": get_cummulative_returns(rewards),
                            }
                    paths.append(path)
                    break
        return paths

    def proc_img(self, img):
        result = img.T
        gray = cv2.cvtColor(img.T, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        # noise removal
        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        # sure background area
        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.01 * dist_transform.max(), 255, 0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Marker labelling
        ret, markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1

        # Now, mark the region of unknown with zero
        markers[unknown == 255] = 0
        result[markers == -1] = [255, 0, 0]
        result[:,:,1] = 50*markers
        return result