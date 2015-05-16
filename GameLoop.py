from Graphics import *
from KeyboardInput import KeyboardInput
from MouseInput import MouseInput
from Surface import Surface
from CollisionDetection import CollisionDetection
from GameTimer import GameTimer

class GameLoop(object):
	def __init__(self, surface, gameUpdate = lambda : None):
		# Input
		self.keyboardInput = KeyboardInput(surface)
		self.mouseInput = MouseInput(surface)

		# The game components
		self.surface = surface
		self.gameUpdate = gameUpdate
		self.physics = CollisionDetection(0, 0, surface.getWidth(), surface.getHeight(), self.surface) 
		
		self.gameTimer = GameTimer(surface,[self.keyboardInput.update, self.mouseInput.update, self.gameUpdate, self.physics])

	def addKeyPressListener(self, handler):
		self.keyboardInput.addKeyPressListener(handler)

	def addKeyReleaseListener(self, handler):
		self.keyboardInput.addKeyReleaseListener(handler)

	def addKeyTypedListener(self, handler):
		self.keyboardInput.addKeyTypedListener(handler)

	def addMouseDownListener(self, handler):
		self.mouseInput.addMouseDownListener(handler)

	def addMouseUpListener(self, handler):
		self.mouseInput.addMouseUpListener(handler)
	
	def addMouseMovementListener(self, handler):
		self.mouseInput.addMouseMovementListener(handler)
	
	def addMouseClickedListener(self, handler):
		self.mouseInput.addMouseClickedListener(handler)

	def add(self, obj):
		self.surface.add(obj)
		self.physics.addBody(obj)

	def repaint(self):
		self.surface.paint()

	def run(self):
		self.gameTimer.run()