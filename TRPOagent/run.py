import gym
import gym_crumb
from agent.agent_TRPO import TRPOAgent

if __name__ == "__main__":
    env = gym.make("crumb-synthetic-v0")
    agent = TRPOAgent(env)
    agent.learn()
    agent.play(env)

    env1 = gym.make("crumb-pick-v0")
    agent.grasp(env1)
    agent.pick(env1)
    agent.putdown(env1)
