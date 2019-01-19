#Copyright (C) 2018, by Jaeyoung Lim, jaeyoung@auterion.com
# 2D quadrotor environment using rate control inputs (continuous control)

#This is free software: you can redistribute it and/or modify
#it under the terms of the GNU Lesser General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
 
#This software package is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Lesser General Public License for more details.

#You should have received a copy of the GNU Leser General Public License.
#If not, see <http://www.gnu.org/licenses/>.


import gym
from gym import error, spaces, utils
from math import cos, sin, pi
import numpy as np

class Quadrotor2D(gym.Env):
	metadata = {'render.modes': ['human']}
	def __init__(self):
		self.mass = 1.0
		self.dt = 0.01
		self.g = np.array([0.0, -9.8])

		self.att = np.array([0.0])
		self.pos = np.array([0.0, 0.0])
		self.vel = np.array([0.0, 0.0])

		self.viewer = None
		self.quadtrans = None
		self.x_range = 1.0


	def step(self, action):
		thrust = action[0] # Thrust command
		w = action[1] # Angular velocity command
		# acc = thrust/self.mass * np.array([cos(self.att + pi()/2), sin(self.att + pi()/2)]) + self.g
		acc = thrust/self.mass * np.array([cos(self.att + pi/2), sin(self.att + pi/2)]) + self.g
		self.vel = self.vel + acc * self.dt
		self.pos = self.pos + self.vel * self.dt + 0.5*acc*self.dt*self.dt
		self.att = self.att + w * self.dt

	def reset(self):
		print("reset")
		#self.state = np.array([self.np_random.uniform(low=-0.6, high=-0.4), 0])
		return np.array(self.state)

	def render(self, mode='human', close=False):
		screen_width = 600
		screen_height = 400

		world_width = self.x_range*2
		scale = screen_width/world_width
		quadwidth = 50.0
		quadheight = 10.0

		if self.viewer is None:
			from gym.envs.classic_control import rendering
			self.viewer = rendering.Viewer(screen_width, screen_height)
			l,r,t,b = -quadwidth/2, quadwidth/2, quadheight/2, -quadheight/2
			quad = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
			self.quadtrans = rendering.Transform()
			quad.add_attr(self.quadtrans)
			self.viewer.add_geom(quad)

		if self.pos is None: return None
		x = self.pos
		theta = self.att
		quad_x = x[0]*scale+screen_width/2.0 # MIDDLE OF CART
		quad_y = x[1]*scale+screen_height/2.0 # MIDDLE OF CART
		self.quadtrans.set_translation(quad_x, quad_y)
		self.quadtrans.set_rotation(theta)

		return self.viewer.render(return_rgb_array = mode=='rgb_array')
