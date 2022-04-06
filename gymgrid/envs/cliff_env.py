import time

import gym
import numpy as np

from .general_grid import *


class Cliff(GridWorld):
    """docstring for Cliff"""

    def __init__(self, world_width=12,
                 world_height=4,
                 unit_pixel=40,
                 default_reward=-1,
                 goal_reward=0,
                 punish_reward=-100,
                 windy=False):
        super().__init__(world_width,
                         world_height,
                         unit_pixel,
                         default_reward,
                         goal_reward,
                         punish_reward,
                         windy)
        self.goal_grid = [(11, 0)]
        for i in range(1, 11):
            self.add_punish(i, 0)


if __name__ == '__main__':
    env = Cliff()
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
            print(observation)
            action = env.action_space.sample()
            observation, reward, done, info = env.step(action)
            time.sleep(0.1)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                env.render()
                time.sleep(0.3)
                break
    env.close()
    print("env closed")
