class ComplexityHandler:
	def __init__(self, complexity=0):
		self.__complexity_levels = {
			0:{'articulation':True, 'fingering':True, 'ties':True, 'slurs':True, 'spacing':False},
			1:{'articulation':True, 'fingering':True, 'ties':True, 'slurs':True, 'spacing':True},
			2:{'articulation':True, 'fingering':False, 'ties':True, 'slurs':True, 'spacing':True},
			3:{'articulation':False, 'fingering':False, 'ties':True, 'slurs':True, 'spacing':True},
			4:{'articulation':False, 'fingering':False, 'ties':True, 'slurs':False, 'spacing':True},
			5:{'articulation':False, 'fingering':False, 'ties':False, 'slurs':False, 'spacing':True}}
		self.curr_complexity = 0

	def retrieve_complexity_settings(self):
		"""Retreive the complexity settings for the current complexity.

		return
		------
			The complexity settings for the current score complexity.

		"""

		return self.__complexity_levels[self.curr_complexity]

	def change_complexity(self, increase):
		"""Change the complexity level of the score.

		args
		----
			increase:
				True if complexity should increase, otherwise false.

		"""

		# Change complexity
		if increase:
			self.curr_complexity += 1
		else:
			self.curr_complexity -= 1

		# Validate complexity
		if self.curr_complexity < min(self.__complexity_levels.keys()):
			self.curr_complexity = min(self.__complexity_levels.keys())
		if self.curr_complexity > max(self.__complexity_levels.keys()):
			self.curr_complexity = max(self.__complexity_levels.keys())

