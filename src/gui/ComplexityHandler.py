class ComplexityHandler:
	def __init__(self, complexity=0):
		self.__complexity_levels = {0:'', 1:'', 2:'', 3:'', 4:'', 5:'', 6:''}
		self.curr_complexity = 0

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

