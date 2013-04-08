import gui

import lilypond as ly

class ScoreModifier:
	def __init__(self, score_file):
		self.score_file = score_file
		self.note_sets = ly.score_tools.create_note_objects(score_file)

		self.spacing_handler = gui.SpacingHandler()
		self.articulation_handler = gui.ArticulationHandler()

	def change_spacing(self, increase):
		"""Change the spacing reference and re-typeset the score.

		args
		----
			increase:
				If true, the spacing reference is multiplied by 2.
				If false, the spacing reference is divided by 2.

		return
		------
			The spaced and typeset score.

		"""

		score = self.spacing_handler.change_spacing(increase, self.score_file)

		return score

	def normalise_spacing(self):
		"""Change the spacing to the best estimate for same-sized bars and typesets the new score.

		return
		------
			The spaced and typeset score.

		"""

		spacing_estimate = ly.spacing_tools.estimate_spacing(self.note_sets)
		score = self.spacing_handler.space_score(spacing_estimate, self.score_file)

		return score

	def toggle_articulation(self):
		"""Toggle articulation of the score.

		If articulation is currently visible, remove articulation.
		If articulation can not currently be seen, make it visible.

		return
		------
			The spaced and typeset score.

		"""

		score = self.articulation_handler.toggle_articulation(self.note_sets)

		return score

