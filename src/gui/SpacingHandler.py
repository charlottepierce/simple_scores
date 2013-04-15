import os

import lilypond as ly

class SpacingHandler:
	def __init__(self, spacing_on=True, algorithm=3, spacing_ref=4):
		"""Create a SpacingHandler object.

		args
		----
			spacing_on:
				The initial value for spacing.

			algorithm:
				The initial spacing algorithm.

			spacing_ref:
				The initial spacing reference.

		"""

		self.curr_spacing_ref = spacing_ref
		self.algorithm = algorithm
		self.spacing_on = spacing_on

	def set_spacing_ref(self, spacing_ref):
		"""Change the spacing reference.

		args
		----
			spacing_ref:
				The new spacing reference.

		"""

		self.curr_spacing_ref = spacing_ref
		if self.curr_spacing_ref < 1:
			self.curr_spacing_ref = 1 # make sure reference is at least 1

	def change_spacing(self, increase):
		"""Change the spacing reference for a score.

		args
		----
			increase:
				If true, the spacing reference is multiplied by 2.
				If false, the spacing reference is divided by 2.

		"""

		if increase:
			self.curr_spacing_ref *= 2
		else:
			self.curr_spacing_ref /= 2

		if self.curr_spacing_ref < 1:
			self.curr_spacing_ref = 1 # make sure reference is at least 1

