import sys
import os
import Tkinter as tk
import Image, ImageTk

def add_proportional_spacing(score_text, spacing_ref):
	"""Add proportional spacing to a score.

	The spacing will be applied to the given score (assumed to be in Lilypond
	notation), using the given value as the reference denominator.
	The reference numerator is 1.

	Proportional spacing is declared for the entire score using a top-level layout
	block as follows:

	\layout {
		\context {
			\Score proportionalNotationDuration = #(ly:make-moment <ref_numerator> <ref_demoninator>)
		}
	}

	TODO: Currently assumes that the score does not already contain a Lilypond layout block.
	TODO: Currently assumes that no other context modifers are currently present in the score.

	args
	----
		score_text:
			The Lilypond notation for the score

		spacing_ref:
			All other music will be spaced against this note value.
			When combined with the numerator (1), represents a note value in terms of
			a fraction of a semibreve.

	return
	------
		Modified version of score_text, with a proportional spacing declaration.

	"""

	return score_text + "\\layout {\\context { \\Score proportionalNotationDuration = #(ly:make-moment 1 %s)}}" % (spacing_ref)

def estimate_spacing(note_sets):
	"""Estimate the optimal spacing for a score.

	The spacing estimated is the fastest not found in those
	given, multiplied by two.

	args
	----
		note_sets:

	return
	-----
		The estimated optimal spacing for the score, within the
		context of trying to make every bar the same size.

	"""

	return max([note.length for note_set in note_sets for note in note_set]) * 2

