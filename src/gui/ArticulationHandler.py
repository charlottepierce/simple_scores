import os

import lilypond as ly

class ArticulationHandler:
	def __init__(self, articulation_on=True, fingering_on=True):
		"""Create an ArticulationHandler object.

		args
		----
			articulation_on:
				The initial state for articulation.

			fingering_on:
				The initial state for fingering marks.
		"""

		self.articulation_on = articulation_on
		self.fingering_on = fingering_on

	def toggle_articulation(self):
		"""Toggle the articulation setting."""

		self.articulation_on = not self.articulation_on

	def toggle_fingering(self):
		"""Toggle the fingering setting."""

		self.fingering_on = not self.fingering_on

