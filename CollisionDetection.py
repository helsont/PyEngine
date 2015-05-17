from QuadTree import QuadTree 
from Body import Body
from Vec2 import Vec2
import time
import math
from Graphics import *
from SweepAndPrune import SweepAndPrune
from LinkedList import *

class CollisionDetection(object):
	def __init__(self, x, y, w, h, *args):
		self.tree = QuadTree(x, y, w, h, 1, args[0])
		self.objects = []
		self.ll = LinkedList()
		self.size = 0
	
	def addBody(self, b):
		if not hasattr(b, "appearance"):
			raise AttributeError("Specify an appearance for each collision body.")
		self.ll.insert(b)
		size += 1
		# self.objects.append(b)

	def getNumBodies(self):
		return self.size
		
	def updateStep(self, delta):
		self.tree.clear()
		
		# Add the bodies to the tree
		idx = 0
		size = self.objects.__len__()

		Node curr = None
		while curr != None
		while idx < size:
			self.tree.insert(self.objects[idx])
			idx += 1

		self.broadphase1(self.objects)

	def broadphase2(self, obj, objects):
		'''Sweep and prune collision detection'''
		sweepAndPrune = SweepAndPrune()
		return sweepAndPrune.getNearest(obj, objects)

	def broadphase1(self, objects):
		'''QuadTree collision detection'''
		detectedCollisions = []
		for x in objects:
			if x.getType() == 'static':
				continue
			possible = self.tree.retrieve(x)

			bodyX = self.getBody(x)

			bodyX.x += bodyX.force.x
			bodyX.y += bodyX.force.y

			bodyX.appearance.x += bodyX.force.x
			bodyX.appearance.y += bodyX.force.y

			self.applyGravity(bodyX)
			self.applyHorizontalFriction(bodyX)

			for y in possible:
				# Run collision detection algorithm
				bodyY = self.getBody(y)
				
				if bodyY is bodyX:
					continue

				if self.isColliding(bodyX, bodyY):
					if bodyY.getType() == 'static':
						# print "Static"
						self.correctStaticCollision(bodyX, bodyY)
						pass
					else :
						self.correctCollision(bodyX, bodyY)
				detectedCollisions.append(Pair(bodyX, bodyY))

	def applyGravity(self, body):
		body.force += Vec2(0, .2)

	def bounce(self, body):

		# if body.y + body.h > self.tree.h - 100: 
		# 	body.force.y = -body.force.y

		if body.x + body.w > self.tree.w:
			body.force.x = -abs(body.force.x)
		elif body.x < 0:
			body.force.x = abs(body.force.x)
		if body.y + body.h > self.tree.h:
			body.force.y = -abs(body.force.y)
		elif body.y < 0:
			body.force.y = abs(body.force.y)
		
	def capSpeed(self, body):
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
		body.force.x -= body.force.x * .1

		# if body.force.x > -.1 and body.force.x < .1:
		# 	body.force.x = math.floor(body.force.x)

		# if body.force.y > -.1 and body.force.y < .1:
		# 	body.force.y = math.floor(body.force.y)

	def isColliding(self, bX, bY):
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

	def correctStaticCollision(self, bx, static):
		diffX = 0
		# if bx.x < static.x: # ok so x is left of y ...
		# 	diffX = static.x + static.w - bx.x

		# 	bx.force.x = -diffX/2
		# else:
		# 	diffX = static.x + static.w - bx.x

		# 	bx.force.x = diffX/2

		diffY = 0
		if bx.y < static.y:
			diffY = bx.y + bx.h - static.y

			bx.force.y = -diffY/2
		else:
			diffY = static.y + static.h - bx.y

			bx.force.y = -diffY/2

	def getBody(self, obj):
		if not isinstance(obj, Body):
			if hasattr(obj, "body"):
				return obj.body
			else: 
				raise ValueError("This object does not have a body attached to it.")
		return obj

class Pair(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b

# insertTime = time.time() * 1000 -  insertTime
# print "insertTime:" + str(insertTime)

# handShakeTime = time.time() * 1000
# For each object, get the possible colliding objects


# handShakeTime = time.time() * 1000 - handShakeTime 
# print "handShakeTime:"+str(handShakeTime)
