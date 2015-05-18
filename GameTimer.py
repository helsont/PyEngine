import time
import sys

class GameTimer(object):
	DEFAULT_FPS = 1
	def __init__(self, surface, processes = None, doNotTime = False):
		'''
		@param processes The objects to update. Each process must 
			have a method "update(self)".
		@param doNotTime The GameTimer automatically adds utility 
			timers for performance testing of each individual process. 
			This is helpful tool for blunt profiling.'''

		self.framesPerSecond = GameTimer.DEFAULT_FPS
		self.maxFramesSkip = 5
		self.totalFramesSkipped = 0
		self.averageFPS = 0
		
		self.framePeriod = 1000 / float(self.framesPerSecond)
		self.framesPerCycle = 0
		self.secondsPerCycle = 0
		self.prevFrameTime = 0

		self.surface = surface
		if not hasattr(processes, "__len__"):
			# Wrapping the singular process in an array
			self.processes = [processes]
		else:
			self.processes = processes

		# Profiling timers
		self.timeProcesses = not doNotTime
		if self.timeProcesses:
			self.timers = []
			self.createTimers(self.processes)

		# Running is whether the game loop is updating.
		self.running = True

		# Paused signifies whether the processes update
		self.paused = False

		# Total number of frames in the entirety of the game
		self.totalFrames = 0

	def createTimers(self, processes):
		if processes == None:
			raise ValueError('Cannot create timer when no ' +
				'processes to time have been provided.')
		anonClass = 0
		for x in processes:
			timerName = ""
			if hasattr(x, 'im_class'):
				# If the update method is defined in a class
				timerName = str(x.im_class)
			else:
				# Give it a default name
				timerName = "anonymousClass_" + str(anonClass)
				anonClass += 1
			self.timers.append(ProcessTimer(timerName))

	def setPause(self, val):
		self.paused = val

	def cycleProcessesWithProfile(self):
		if not self.processes == None:
			idx = 0
			size = self.processes.__len__()

			while idx < size:
				
				if hasattr(self.processes[idx], "__call__"):
					# If it's a function
					self.timers[idx].start()
					self.processes[idx]()
					self.timers[idx].stop()
				elif hasattr(self.processes[idx], "update"):
					# If it's an object
					self.timers[idx].start()
					self.processes[idx].update()
					self.timers[idx].stop()
				elif hasattr(self.processes[idx], "updateStep"):
					# If it's a function
					self.timers[idx].start()
					self.processes[idx].updateStep(self.prevFrameTime)
					self.timers[idx].stop()
				idx += 1

	def cycleProcesses(self):
		if not self.processes == None:
			idx = 0

			for x in self.processes:
				self.processes[idx]()

	def getTimerStats(self):
		if self.timeProcesses == False:
			raise ValueError('Cannot obtain timer ' +
				'stats when attribute doNotTime is False')
		res = []
		idx = 0
		while idx < self.timers.__len__():
			res.append(self.timers[idx].stats)
			idx+=1

		return res

	def updateAll(self):
		if not self.paused:
			# Only update everything
			if self.timeProcesses:
				self.cycleProcessesWithProfile()
			else:
				self.cycleProcesses()

	def getTimerName(self, idx):
		return self.timers[idx].name

	def run(self):
		beginTime = 0
		timeDiff = 0
		sleepTime = 0
		self.secondsPerCycle = time.time() * 1000
		framesSkipped = 0
		
		while self.running:
			beginTime = time.time() * 1000

			self.updateAll()

			self.surface.update()

			# Update the timers
			timeDiff = time.time() * 1000 - beginTime
			sleepTime = self.framePeriod - timeDiff
			self.prevFrameTime = timeDiff

			if sleepTime > 0:
				# Performance is good, sleepTime is positive
				time.sleep(sleepTime / 1000)
			else:
				# Skip several visual frames
				while sleepTime < 0 and framesSkipped < 5:
					framesSkipped += 1
					sleepTime += self.framePeriod

					# Force updates, no repaints
					self.updateAll()
					
			self.totalFrames += 1
			self.framesPerCycle += 1
			if self.framesPerCycle == self.framesPerSecond:
				now = time.time() * 1000
				
				self.averageFPS = (now - self.secondsPerCycle) * self.framesPerSecond/1000
				
				# Reset these
				self.secondsPerCycle = time.time() * 1000
				self.framesPerCycle = 0

				banger = time.time() * 1000
				self.totalFramesSkipped += framesSkipped
				# print("FPS:" + str(self.averageFPS))

			if self.totalFrames % 20 == 0:
				s = Statistics.findLargestAverageRun(self.getTimerStats())
				# print self.getTimerName(s[0]) + " longest at " + str(s[1]) + " ms."
				print Statistics.getAverages([self.getTimerStats()[3]])[0][1]
			self.running = False

class ProcessTimer(object):
	# The number of stat cycles to store
	STAT_SIZE = 100
	def __init__(self, name, statSize = STAT_SIZE):
		self.name = name
		self.totalTime = 0
		self.startTime = 0
		self.stats = [None] * statSize
		self.statSize = statSize
		self.currIdx = 0

	def start(self):
		self.startTime = time.time() * 1000

	def stop(self):
		self.stats[self.currIdx % self.statSize] = time.time() * 1000 - self.startTime
		self.currIdx += 1

class Statistics(object):
	def __init__(self):
		pass

	@staticmethod
	def getAverages(vals):
		runIdx = 0
		averages = []
		while runIdx < vals.__len__():

			currAverage = 0
			valIdx = 0

			while valIdx < vals[runIdx].__len__():
				if vals[runIdx][valIdx] == None:
					break
				currAverage += vals[runIdx][valIdx]
				valIdx += 1
			
			currAverage /= valIdx
			averages.append([runIdx, currAverage])

			runIdx += 1

		return averages
	@staticmethod
	def findLargestAverageRun(vals):
		'''@param vals Expects a 2D array with the first dimension 
				representing one run and the second dimension containing 
				the values of that run.
			@returns A tuple where the 0th index is the run index and 
				the 1st index is the largest average.

			Example: vals = [[2, 10.1, 4.33, 1], [8, 9.7, 9, 6]]'''

		largest = -sys.maxint - 1
		largestIndex = -1

		runIdx = 0

		while runIdx < vals.__len__():

			average = 0
			valIdx = 0

			while valIdx < vals[runIdx].__len__():
				if vals[runIdx][valIdx] == None:
					break
				average += vals[runIdx][valIdx]
				valIdx += 1
			
			average /= valIdx

			if average > largest:
				largest = average
				largestIndex = runIdx

			runIdx += 1

		return [largestIndex, largest]