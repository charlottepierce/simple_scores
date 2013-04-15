import os

import gui
import lilypond as ly

class ScoreModifier:
	def __init__(self, score_file):
		self.score_file = score_file
		self.note_sets = ly.score_tools.create_note_objects(score_file)

		self.spacing_handler = gui.SpacingHandler()
		self.articulation_handler = gui.ArticulationHandler()
		self.joins_handler = gui.JoinsHandler()

	def typeset_score(self):
		"""Typeset the score using the current settings (i.e., spacing, articulation etc.).

		return
		------
			The typeset score.

		"""

		tmp_score = '.to-typeset.ly'

		# Save score to temporary file
		articulation = self.articulation_handler.articulation_on
		fingering = self.articulation_handler.fingering_on
		ties = self.joins_handler.ties_on
		slurs = self.joins_handler.slurs_on
		ly.score_tools.save_score(self.note_sets, tmp_score, articulation=articulation, fingering=fingering, ties=ties, slurs=slurs)
		# Apply spacing
		score_text = open(tmp_score).read()
		spaced_score = ly.spacing_tools.add_proportional_spacing(score_text, self.spacing_handler.curr_spacing_ref)

		# Save spaced score, typeset, remove score
		open(tmp_score, 'w+').write(spaced_score)
		typeset_score = ly.typesetting_tools.typeset_score(tmp_score, 'png')
		os.remove(tmp_score)

		return typeset_score

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

		self.spacing_handler.change_spacing(increase)

		return self.typeset_score()

	def normalise_spacing(self):
		"""Change the spacing to the best estimate for same-sized bars and typesets the new score.

		return
		------
			The spaced and typeset score.

		"""

		spacing_estimate = ly.spacing_tools.estimate_spacing(self.note_sets, algorithm=self.spacing_handler.algorithm)
		self.spacing_handler.set_spacing_ref(spacing_estimate)

		return self.typeset_score()

	def toggle_articulation(self):
		"""Toggle articulation of the score.

		If articulation is currently visible, remove articulation.
		If articulation can not currently be seen, make it visible.

		return
		------
			The spaced and typeset score.

		"""

		self.articulation_handler.toggle_articulation()

		return self.typeset_score()

	def toggle_fingering(self):
		"""Toggle fingering of the score.

		If fingering is currently visible, remove fingering.
		If fingering can not currently be seen, make it visible.

		return
		------
			The spaced and typeset score.

		"""

		self.articulation_handler.toggle_fingering()

		return self.typeset_score()

	def toggle_ties(self):
		"""Toggle ties on the score.

		If ties are currently visible, remove ties.
		If ties can not currently be seen, make them visible.

		return
		------
			The spaced and typeset score.

		"""

		self.joins_handler.toggle_ties()

		return self.typeset_score()

	def toggle_slurs(self):
		"""Toggle slurs on the score.

		If slurs are currently visible, remove slurs.
		If slurs can not currently be seen, make them visible.

		return
		------
			The spaced and typeset score.

		"""

		self.joins_handler.toggle_slurs()

		return self.typeset_score()

