from QuadTree import QuadTree
from Body import Body
import pdb
import random

tree = QuadTree(0, 0, 400, 400, 1)

for p in range(0,4):
	print p
	# print "Inserting" + str(x)
	# if x == 4:
		# pdb.set_trace()
	x = random.randrange(0, tree.w - 10)
	y = random.randrange(0, tree.h/2 - 10)
	tree.insert(Body(x, y, 10, 10))

bobby = Body(195,150,10,10)
bobby.name = "Bobby"
tree.insert(bobby)

pdb.set_trace()
possible = tree.retrieve(bobby)

for x in possible:
	print x.toString()