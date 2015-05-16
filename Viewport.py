import math

class Viewport(object):
	def __init__(self, x, y, width, height, follow = None):
		self.worldX = x
		self.worldX = y
		self.worldWidth = width
		self.worldHeight = height

		self.viewX = x
		self.viewY = y
		self.viewWidth = 400
		self.viewHeight = 400

		self.follow = follow

	def track(self, obj):
		self.follow = obj
		app = self.follow.body.appearance
		
		self.viewX = app.x - self.viewWidth/2
		self.viewY = app.y - self.viewHeight/2

	def update(self):
		self.viewX = self.follow.appearance.x - self.viewWidth/2
		self.viewY = self.follow.appearance.y - self.viewHeight/2

		# Prevent offscreen viewport
		self.viewX = math.min(self.viewX, 0)
		self.viewY = math.min(self.viewY, 0)

	def getViewX(self):
		return self.viewX

	def getViewY(self):
		return self.viewY