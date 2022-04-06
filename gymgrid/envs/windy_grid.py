import time

import gym
import numpy as np

from .general_grid import *


class WindyGridWorld(GridWorld):
    """docstring for WindyGridWorld"""

    def __init__(self, world_width=10,
                 world_height=7,
                 unit_pixel=40,
                 default_reward=-1,
                 goal_reward=-1,
                 punish_reward=-10,
                 windy=True):
        super().__init__(world_width,
                         world_height,
                         unit_pixel,
                         default_reward,
                         goal_reward,
                         punish_reward,
                         windy)
        self.goal_grid = [(7, 3)]
        self.start_grid = [(0, 3)]
        self.wind = np.array([0, 0, 0, 1, 1, 1, 2, 2, 1, 0])
        self.action_space = gym.spaces.Discrete(8)


if __name__ == '__main__':
    env = WindyGridWorld()
    # nfs = env.observation_space
    # print(nfs)
    # nfa = env.action_space
    # print("nfs:%s; nfa:%s"%(nfs,nfa))
    # print(env.observation_space)
    # print(env.action_space)
    # print(env.state)
    for i_episode in range(20):
        observation = env.reset()
        for t in range(100):
            env.render()
            # print(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            time.sleep(0.2)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                # env.render()
                time.sleep(1.0)
                break
    env.close()
    print("env closed")
