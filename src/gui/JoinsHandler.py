class JoinsHandler:
	def __init__(self, ties_on=True, slurs_on=True):
		"""Create a JoinsHandler object.

		args
		----
			ties_on:
				The initial state for tie marks.

			slurs_on:
				The initial state for slur marks.

		"""

		self.ties_on = ties_on
		self.slurs_on = slurs_on

	def toggle_ties(self):
		"""Toggle the tie markings setting."""

		self.ties_on = not self.ties_on

	def toggle_slurs(self):
		"""Toggle the slur markings setting."""

		self.slurs_on = not self.slurs_on

