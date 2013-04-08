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

	def toggle_articulation(self, note_sets):
		"""Toggle the articulation setting for a score, re-typeset score.

		args
		----
			note_sets:
				The set of notes defining the score to modify and typeset.

		return
		------
			File name of the newly spaced and typeset score.

		"""

		self.articulation_on = not self.articulation_on

		# Save score temporarily and typeset
		score_file = '.articulated_score.tmp'
		ly.score_tools.save_score(note_sets, score_file, articulation=self.articulation_on)
		typeset_score = ly.typesetting_tools.typeset_score(score_file, 'png')
		os.remove(score_file)

		return typeset_score

