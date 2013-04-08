import os

import lilypond as ly

class ArticulationHandler:
	def __init__(self, articulation_on=True):
		"""Create an ArticulationHandler object.

		args
		----
			articulation_on:
				The initial state for articulation.
		"""

		self.articulation_on = articulation_on

	def toggle_articulation(self):
		"""Toggle the articulation setting."""

		self.articulation_on = not self.articulation_on

