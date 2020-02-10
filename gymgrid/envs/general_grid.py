import gym
import numpy as np
from gym.envs.classic_control import rendering

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
					   windy = False):
		super(GridWorld, self).__init__()
		self.world_width = world_width
		self.world_height = world_height
		self.unit_pixel = unit_pixel
		self.default_reward = default_reward
		self.goal_reward = goal_reward
		self.punish_reward = punish_reward

		# spaces
		# 0,1,2,3,4: left, right, up, down and -
		self.action_space = gym.spaces.Discrete(4)
		# self.observation_space = gym.spaces.Discrete(self.world_height*self.world_width)
		self.observation_space = gym.spaces.MultiDiscrete([self.world_width, self.world_height])

		# special grids
		self.start_grid = [(0,0)]	# default start point
		self.punish_grids = []	# reward value: punish_reward, start from (0,0)
		self.goal_grid = [(self.world_width-1, 0)]		# reward value: goal_reward
		# GUI
		self.viewer = None
		self.state = None
		# self.steps_beyond_done = None

	def render(self, mode='human'):
		unit_pixel = self.unit_pixel
		if self.viewer is None:
			self.viewer = rendering.Viewer(self.world_width*unit_pixel, self.world_height*unit_pixel)
			# Draw lines
			for c in range(0, self.world_width*unit_pixel, unit_pixel):
				x0, y0, x1, y1 = c, 0, c, self.world_height*unit_pixel
				l = rendering.Line((x0,y0), (x1,y1))
				l.set_color(0,0,0)
				self.viewer.add_geom(l)
			for r in range(0, self.world_height*unit_pixel, unit_pixel):
				x0, y0, x1, y1 =  0, r, self.world_width*unit_pixel, r
				l.set_color(0,0,0)
				l = rendering.Line((x0,y0), (x1,y1))
				self.viewer.add_geom(l)

			origin = np.array([unit_pixel/2, unit_pixel/2])
			gap = 2 # 5 pixels gap between object and line
			# Draw cliff: black rect
			for i in range(len(self.punish_grids)):
				(x,y) = self.punish_grids[i]
				v = [(x*unit_pixel+gap, y*unit_pixel+gap),
	                 ((x+1)*unit_pixel-gap, y*unit_pixel+gap),
	                 ((x+1)*unit_pixel-gap, (y+1)*unit_pixel-gap),
	                 (x*unit_pixel+gap, (y+1)*unit_pixel-gap)
				]
				rect = rendering.FilledPolygon(v)
				rect.set_color(0,0,0)
				self.viewer.add_geom(rect)
			# Draw goal: yellow oval
			self.goals = []
			for i in range(len(self.goal_grid)):
				goal = rendering.make_circle((unit_pixel-2*gap)/2)
				goal.set_color(1,1,0) # yellow
				goal_x, goal_y = self.goal_grid[i] 
				goal_location = origin + np.array([unit_pixel*goal_x, unit_pixel*goal_y])
				circletrans = rendering.Transform(translation=(goal_location[0],goal_location[1]))
				goal.add_attr(circletrans)
				self.viewer.add_geom(goal)
				self.goals.append(goal)
			# Draw agent: red rect
			startx = self.start_grid[0][0]
			starty = self.start_grid[0][1]
			agent_stlocation = [(gap+startx*unit_pixel,gap+starty*unit_pixel),
								(unit_pixel-gap+startx*unit_pixel, gap+starty*unit_pixel),
								(unit_pixel-gap+startx*unit_pixel, unit_pixel-gap+starty*unit_pixel),
								(gap+startx*unit_pixel, unit_pixel-gap+starty*unit_pixel)]
			self.agent = rendering.FilledPolygon(agent_stlocation)
			self.agent.set_color(1.0, 0, 0.0)	# red
			self.viewer.add_geom(self.agent)
			self.agent_trans = rendering.Transform()
			self.agent.add_attr(self.agent_trans)
		if self.state is None: return None
		x = self.state[0]
		y = self.state[1]
		self.agent_trans.set_translation(x*unit_pixel, y*unit_pixel)
		return self.viewer.render(return_rgb_array=mode == 'rgb_array')

	def step(self, action):
		assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
		self.action = action
		old_x = self.state[0]
		old_y = self.state[1]
		new_x, new_y = old_x, old_y
		if action == 0: new_x -= 1   # left
		elif action == 1: new_x += 1   # right
		elif action == 2: new_y += 1   # up
		elif action == 3: new_y -= 1   # down
		elif action == 4: new_x,new_y = new_x-1,new_y-1
		elif action == 5: new_x,new_y = new_x+1,new_y-1
		elif action == 6: new_x,new_y = new_x+1,new_y-1
		elif action == 7: new_x,new_y = new_x+1,new_y+1
        # boundaries
		if new_x < 0: new_x = 0
		if new_x >= self.world_width: new_x = self.world_width-1
		if new_y < 0: new_y = 0
		if new_y >= self.world_height: new_y = self.world_height-1

		if (new_x, new_y) in self.goal_grid:
			done = True
			reward = self.goal_reward
		elif (new_x, new_y) in self.punish_grids:
			done = True
			reward = self.punish_reward
		else:
			done = False
			reward = self.default_reward
		# if done:
		# 	self.state = None
		# else: 
		# 	self.state = np.array([new_x, new_y])
		self.state = np.array([new_x, new_y])
		return self.state, reward, done, {}  


	def reset(self):
		# set all girds normal
		# clear punish_grids and goal grid
		startx = self.start_grid[0][0]
		starty = self.start_grid[0][1]
		self.state = np.array([startx,starty])
		return self.state


	def add_punish(self,x,y):
		self.punish_grids.append((x,y))

	def add_goal(self,x,y):
		self.goal_grid.append((x,y))

	def set_start(self,x,y):
		self.start_grid = [(x,y)]
	

	def close(self):
		if self.viewer:
			self.viewer.close()
			self.viewer = None


