class SweepAndPrune(object):
	def __init__(self):
		pass

	def getNearest(self, obj, possibles):
		sortedByXAxis = sorted(possibles, key=lambda body: body.x)
		midpoint = sortedByXAxis.__len__()
		lowerBound = midpoint
		upperBound = midpoint

		x = obj.x
		y = obj.y
		mX = obj.w + x
		mY = obj.h + y
		while sortedByXAxis[lowerBound].x + sortedByXAxis[lowerBound].w > x
			lowerBound -= 1

		while sortedByXAxis[upperBound].x < mX
			upperBound += 1

		return sortedByXAxis[lowerBound:upperBound]