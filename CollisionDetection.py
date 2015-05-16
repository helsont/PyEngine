from QuadTree import QuadTree 
from Body import Body
from Vec2 import Vec2
import time
import math
from Graphics import *

class CollisionDetection(object):
	def __init__(self, x, y, w, h, *args):
		self.tree = QuadTree(x, y, w, h, 1)
		self.objects = []
	
	def addBody(self, b):
		if not hasattr(b, "appearance"):
			raise AttributeError("Specify an appearance for each collision body.")
		self.objects.append(b)

	def getNumBodies(self):
		return self.objects.__len__()
		
	def updateStep(self, delta):
		self.tree.clear()
		insertTime = time.time() * 1000
		
		# Add the bodies to the tree
		idx = 0
		size = self.objects.__len__()

		while idx < size:
			self.tree.insert(self.objects[idx])
			idx += 1

		# insertTime = time.time() * 1000 -  insertTime
		# print "insertTime:" + str(insertTime)

		# handShakeTime = time.time() * 1000
		# For each object, get the possible colliding objects
		for x in self.objects:
			possible = self.tree.retrieve(x)

			bodyX = self.getBody(x)

			# if bodyX.name == "Michelle":
				# self.applyHorizontalFriction(body)
				# self.applyGravity(bodyX)

			bodyX.x += bodyX.force.x
			bodyX.y += bodyX.force.y

			bodyX.appearance.x += bodyX.force.x
			bodyX.appearance.y += bodyX.force.y

			self.bounce(bodyX)

			for y in possible:
				# Run collision detection algorithm
				bodyY = self.getBody(y)
				
				if bodyY is bodyX:
					continue
				if self.narrowphase(bodyX, bodyY):
					self.correctCollision(bodyX, bodyY)

		# handShakeTime = time.time() * 1000 - handShakeTime 
		# print "handShakeTime:"+str(handShakeTime)
	
	def applyGravity(self, body):
		body.force += Vec2(0, .2)

	def bounce(self, body):
		if body.name == "Michelle":
			self.applyHorizontalFriction(body)

		# if body.y + body.h > self.tree.h - 100: 
		# 	body.force.y = -body.force.y

		# Cap speed
		maxspeed = 10
		if body.force.x > maxspeed:
			body.force.x = maxspeed
		if body.force.x < -maxspeed:
			body.force.x = -maxspeed
		if body.force.y > maxspeed:
			body.force.y = maxspeed
		if body.force.y < -maxspeed:
			body.force.y = -maxspeed

	def applyHorizontalFriction(self, body):
		body.force -= body.force * .01

		if body.force.x > -.1 and body.force.x < .1:
			body.force.x = math.floor(body.force.x)

		if body.force.y > -.1 and body.force.y < .1:
			body.force.y = math.floor(body.force.y)
		
	def midphase(self, bX, bY):
		length = bX.x - bY.x
		halfWX = bX.w/2
		halfWY = bY.x/2

		gap = length - halfWX - halfWY
		
		return gap <= 0 

	def narrowphase(self, bX, bY):
		myx1 = bX.x #left
		myy1 = bX.y #top
		myx2 = bX.x + bX.w #right
		myy2 = bX.y + bX.h #bottom

		otherx1 = bY.x #left
		othery1 = bY.y #top
		otherx2 = bY.x + bY.w #right
		othery2 = bY.y + bY.h #bottom
		return  myy1 < othery2 and myy2 > othery1 and myx1 < otherx2 and myx2 > otherx1

	def correctCollision(self, bx, by):
		diffX = 0
		if bx.x < by.x: # ok so x is left of y ...
			diffX = by.x + by.w - bx.x

			bx.force.x = -diffX/2
			by.force.x = diffX/2
		else:
			diffX = by.x + by.w - bx.x

			bx.force.x = diffX/2
			by.force.x = -diffX/2

		diffY = 0
		if bx.y < by.y: # ok so x is left of y ...
			diffY = bx.y + bx.h - by.y

			bx.force.y = -diffY/2
			by.force.y = diffY/2
		else:
			diffY = by.y + by.h - bx.y

			bx.force.y = -diffY/2
			by.force.y = diffY/2

	def getBody(self, obj):
		if not isinstance(obj, Body):
			if hasattr(obj, "body"):
				return obj.body
			else: 
				raise ValueError("This object does not have a body attached to it.")
		return obj