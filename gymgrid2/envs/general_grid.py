import gym
import numpy as np


class GridWorld(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 2
    }

    def __init__(self, world_width=12,
                 world_height=4,
                 unit_pixel=40,
                 default_reward=-1,
                 goal_reward=100,
                 punish_reward=-10,
                 windy=False):
        super(GridWorld, self).__init__()
        self.world_width = world_width
        self.world_height = world_height
        self.unit_pixel = unit_pixel
        self.default_reward = default_reward
        self.goal_reward = goal_reward
        self.punish_reward = punish_reward

        self.windy = windy
        if self.windy:
            self.wind = np.zeros(world_width)

        # spaces
        # 0,1,2,3,4: left, right, up, down and -
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Discrete(
            self.world_height*self.world_width)
        # self.observation_space = gym.spaces.MultiDiscrete([self.world_width, self.world_height])
        # special grids
        self.start_grid = [(0, 0)]  # default start point
        self.punish_grids = []  # reward value: punish_reward, start from (0,0)
        self.goal_grid = [(self.world_width-1, 0)]		# reward value: goal_reward
        # GUI
        self.screen = None
        self.state = None
        self.clock = None
        # self.steps_beyond_done = None

    def render(self, mode='human'):
        import pygame
        from pygame import gfxdraw

        world_width = self.world_width
        world_height = self.world_height
        unit_pixel = self.unit_pixel

        screen_width = world_width*unit_pixel
        screen_height = world_height*unit_pixel

        scale = screen_width/world_width
        if self.state is None:
            return None

        #x = self.state

        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(
                (screen_width, screen_height))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        # Check if close button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                done = True
                return done

        self.surf = pygame.Surface((screen_width, screen_height))
        self.surf.fill((255, 255, 255))
        # draw lines on the screen for the pixels
        for i in range(world_width):
            gfxdraw.vline(self.surf, i*unit_pixel, 0, screen_height, (0, 0, 0))
        for i in range(world_height):
            gfxdraw.hline(self.surf, 0, screen_width, i*unit_pixel, (0, 0, 0))
        gap = 2
        # Draw cliff as a black rectangle
        for i in range(len(self.punish_grids)):
            x, y = self.punish_grids[i]
            gfxdraw.box(self.surf, (x*unit_pixel+gap, y*unit_pixel+gap,
                                    unit_pixel-2*gap, unit_pixel-2*gap), (0, 0, 0))
        # draw the goals as a yellow filled oval
        for i in range(len(self.goal_grid)):
            x, y = self.goal_grid[i]
            gfxdraw.filled_circle(self.surf, x*unit_pixel+unit_pixel//2, y *
                                  unit_pixel+unit_pixel//2, unit_pixel//2 - 2*gap, (255, 255, 0))
        # draw the agent as a red rectangle
        agent_x, agent_y = self.state
        #print(agent_x, agent_y)
        gfxdraw.box(self.surf, (agent_x*unit_pixel+gap, agent_y *
                                unit_pixel+gap, unit_pixel-2*gap, unit_pixel-2*gap), (255, 0, 0))
        # flip y axis
        #self.screen.blit(pygame.transform.flip(self.surf, False, True), (0, 0))
        self.screen.blit(self.surf, (0, 0))
        # pygame.display.flip()
        if mode == 'human':
            pygame.event.pump()
            self.clock.tick(10)
            pygame.display.flip()
        if mode == 'rgb_array':
            return np.transpose(np.array(pygame.surfarray.pixels3d(self.screen)), (1, 0, 2))
        return False

    def step(self, action):
        assert self.action_space.contains(
            action), "%r (%s) invalid" % (action, type(action))
        self.action = action
        old_x = self.state[0]
        old_y = self.state[1]
        new_x, new_y = old_x, old_y

        if self.windy:
            new_y += self.wind[new_x]

        # boundaries
        if action == 0:
            new_x -= 1   # left
        elif action == 1:
            new_x += 1   # right
        elif action == 2:
            new_y += 1   # up
        elif action == 3:
            new_y -= 1   # down
        elif action == 4:
            new_x, new_y = new_x-1, new_y+1
        elif action == 5:
            new_x, new_y = new_x+1, new_y+1
        elif action == 6:
            new_x, new_y = new_x-1, new_y-1
        elif action == 7:
            new_x, new_y = new_x+1, new_y-1

        # boundaries
        if new_x < 0:
            new_x = 0
        if new_x >= self.world_width:
            new_x = self.world_width-1
        if new_y < 0:
            new_y = 0
        if new_y >= self.world_height:
            new_y = self.world_height-1

        if (new_x, new_y) in self.goal_grid:
            done = True
            reward = self.goal_reward
            self.state = np.array([new_x, new_y])
        elif (new_x, new_y) in self.punish_grids:
            done = False
            reward = self.punish_reward
            self.state = np.array([new_x, new_y])
            self.state = np.array(
                [self.start_grid[0][0], self.start_grid[0][1]])
        else:
            done = False
            reward = self.default_reward
            self.state = np.array([new_x, new_y])

        return self.get_obs(), reward, done, {}
        # return self.state, reward, done, {}

    def reset(self):
        # set all girds normal
        # clear punish_grids and goal grid
        startx = self.start_grid[0][0]
        starty = self.start_grid[0][1]
        self.state = np.array([startx, starty])
        return self.get_obs()
        # return self.state

    def get_obs(self):
        return self.state[0]*self.world_height + self.state[1]

    def add_punish(self, x, y):
        self.punish_grids.append((x, y))

    def add_goal(self, x, y):
        self.goal_grid.append((x, y))

    def set_start(self, x, y):
        self.start_grid = [(x, y)]

    def close(self):
        if self.screen:
            import pygame

            pygame.display.quit()
            pygame.quit()
            self.isopen = False
