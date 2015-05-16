class KeyboardInput(object):
	PRESS_TIME = 2

	def __init__(self, surface):
		self.window = surface.window
		self.onKeyPress = None
		self.onKeyRelease = None
		self.onKeyTyped = None
		self.pressed = False
		self.pressTime = 0

	def addKeyPressListener(self, handler):
		self.onKeyPress = handler

	def addKeyReleaseListener(self, handler):
		self.onKeyRelease = handler

	def addKeyTypedListener(self, handler):
		self.onKeyTyped = handler

	def update(self):
		if not self.onKeyPress == None:
			self.onKeyPress(self.window)

		if not self.onKeyRelease == None:
			self.onKeyRelease(self.window)

		if not self.onKeyTyped == None:
			if self.window.getKeyPressed() and not self.pressed:
				self.pressTime += 1
				if self.pressTime >= KeyboardInput.PRESS_TIME:
					self.onKeyTyped(self.window)
					self.pressTime = 0
					self.pressed = True
			if not self.window.getKeyPressed():
				self.pressed = False
				self.pressTime = 0

# class TimedAction(object):
# 	STATE_DOWN = "down"
# 	STATE_UP = "up"
# 	CLICK_TIME = 2

# 	def __init__(self, surface):
# 		self.window = surface.window
# 		self.onMouseDown = None
# 		self.onMouseUp = None
# 		self.onMouseMovement = None
# 		self.onMouseClick = None
# 		self.pressTime = 0
# 		self.clicked = False

# 	def update(self):
# 		if not self.onMouseClick == None:
# 			if self.window.getMouseState() == MouseInput.STATE_DOWN and not self.clicked:
# 				self.pressTime += 1
# 				if self.pressTime >= MouseInput.CLICK_TIME:
# 					self.onMouseClick(self.window)
# 					self.pressTime = 0
# 					self.clicked = True
# 			if self.window.getMouseState() == MouseInput.STATE_UP:
# 				self.clicked = False
# 				self.pressTime = 0