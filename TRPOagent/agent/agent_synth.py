from util import *
import numpy as np
from network.network_synth import NetworkSynth
import rospy
from agent.agent_TRPO import TRPOAgent


class AgentSynth(TRPOAgent):
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
        self.net = NetworkSynth(self.n_actions, self.observation_shape)

    def rollout(self, max_pathlength=2500, n_timesteps=50000):
        paths = []
        total_timesteps = 0
        self.env.state = np.zeros(4)
        while total_timesteps < n_timesteps:
            observations, actions, rewards, action_m, action_logstd = [], [], [], [], []
            observation = self.env.reset()
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

    def grasp(self, env):
        if env:
            print(True)
        obs = synthetic_state(env, env.render(mode='human'), env.aim)
        done = False
        reward = 0
        l = 0
        while done is not True:
            env.gripper.publish(2.0)
            a = self.act(obs, sample=False)[0]
            for i in range(self.n_actions):
                obs, r, done = env.step([i, a[i]])
                obs = synthetic_state(env, obs, env.aim)
                if done:
                    break
            reward += r
            l += 1
            print(l, ')', r, obs, a)
        env.gripper.publish(0.0)
        rospy.sleep(10.0)

    def pick(self, env):
        env.gripper.publish(0.0)
        env.h += 0.2
        obs = synthetic_state(env, env.render(mode='human'), env.aim)

        done = False
        reward = 0
        l = 0
        while done is not True:
            a = self.act(obs, sample=False)[0]
            for i in range(self.n_actions):
                obs, r, done = env.step([i, a[i]])
                obs = synthetic_state(env, obs, env.aim)
                if done:
                    break
            reward += r
            l += 1
            print(l, ')', r, obs, a)

    def putdown(self, env):
        obs = synthetic_state(env, env.render(mode='human'), env.aim)
        env.h += -0.1
        done = False
        reward = 0
        l = 0
        while done is not True:
            a = self.act(obs, sample=False)[0]
            for i in range(self.n_actions):
                obs, r, done = env.step([i, a[i]])
                obs = synthetic_state(env, obs, env.aim)
                if done:
                    break
            reward += r
            l += 1
            print(l, ')', r, obs, a)

