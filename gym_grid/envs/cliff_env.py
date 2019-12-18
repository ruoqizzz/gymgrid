import gym
import numpy as np
from gym.envs.classic_control import rendering
from general_grid import *

def Cliff():
    env = GridWorld()
    env.action_space = gym.spaces.Discrete(4)
    env.goal_grid = [(11,0)]
    for i in range(1,11):
        env.add_punish(i,0)
    return env


if __name__ == '__main__':
    env = Cliff()
    # nfs = env.observation_space
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
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                break
    env.close()
    print("env closed")