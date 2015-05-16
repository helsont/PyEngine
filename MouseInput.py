class MouseInput(object):
	STATE_DOWN = "down"
	STATE_UP = "up"
	CLICK_TIME = 2

	def __init__(self, surface):
		self.window = surface.window
		self.onMouseDown = None
		self.onMouseUp = None
		self.onMouseMovement = None
		self.onMouseClick = None
		self.pressTime = 0
		self.clicked = False

	def addMouseDownListener(self, handler):
		self.onMouseDown = handler

	def addMouseUpListener(self, handler):
		self.onMouseUp = handler

	def addMouseMovementListener(self, handler):
		self.onMouseMovement = handler

	def addMouseClickedListener(self, handler):
		self.onMouseClick = handler

	def update(self):
		if not self.onMouseDown == None:
			if self.window.getMouseState() == MouseInput.STATE_DOWN:
				self.onMouseDown(self.window)

		if not self.onMouseUp == None:
			if self.window.getMouseState() == MouseInput.STATE_UP:
				self.onMouseUp(self.window)

		if not self.onMouseMovement == None:
			self.onMouseMovement(self.window)

		if not self.onMouseClick == None:
			if self.window.getMouseState() == MouseInput.STATE_DOWN and not self.clicked:
				self.pressTime += 1
				if self.pressTime >= MouseInput.CLICK_TIME:
					self.onMouseClick(self.window)
					self.pressTime = 0
					self.clicked = True
			if self.window.getMouseState() == MouseInput.STATE_UP:
				self.clicked = False
				self.pressTime = 0