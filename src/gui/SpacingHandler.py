import os

import lilypond as ly

class SpacingHandler:
	def __init__(self, spacing_ref=1):
		"""Create a SpacingHandler object.

		args
		----
			spacing_ref:
				The initial spacing reference.
		"""

		self.curr_spacing_ref = spacing_ref

	def change_spacing(self, increase, score_file):
		"""Change the spacing reference for a score, re-typeset score.

		Generates a temporary file to store the Lilypond-encoded spaced score.
		This file should be removed by the method.

		args
		----
			increase:
				If true, the spacing reference is multiplied by 2.
				If false, the spacing reference is divided by 2.

			score_file:
				The Lilypond file containing the score to space.

		return
		------
			File name of the newly spaced and typeset score.

		"""

		# Apply spacing change
		if increase:
			self.curr_spacing_ref *= 2
		else:
			self.curr_spacing_ref /= 2

		if self.curr_spacing_ref < 1: self.curr_spacing_ref = 1 # make sure reference is at least 1

		# Read original score, add spacing
		score_text = open(score_file).read()
		spaced_score = ly.spacing_tools.add_proportional_spacing(score_text, self.curr_spacing_ref)

		# Save spaced score temporarily and typeset
		spaced_score_file = '.spaced_score.tmp'
		open(spaced_score_file, 'w+').write(spaced_score)
		typeset_score = ly.typesetting_tools.typeset_score(spaced_score_file, 'png')
		os.remove(spaced_score_file)

		return typeset_score

