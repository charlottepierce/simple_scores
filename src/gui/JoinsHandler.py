class JoinsHandler:
	def __init__(self, ties_on=True):
		"""Create a JoinsHandler object.

		args
		----
			ties_on:
				The initial state for tie marks.

		"""

		self.ties_on = ties_on

	def toggle_ties(self):
		"""Toggle the tie markings setting."""

		self.ties_on = not self.ties_on

