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

def estimate_spacing(note_sets, algorithm=3):
	"""Estimate the optimal spacing for a score.

	If a valid algorithm is not selected, a spacing of 4 is returned.

	args
	----
		note_sets:
			List of lists of note objects.

		algorithm:
			The spacing algorithm to use.
			1: Most frequent note x 2.
			2: Fastest note in score.
			3: Fastest note in score x 2.

	return
	-----
		The estimated optimal spacing for the score, within the
		context of trying to make every bar the same size.

	"""

	if algorithm == 1:
		notes = [note.length for note_set in note_sets for note in note_set] # expanded list of all notes in score
		note_types = set(notes) # set of note lengths found in score
		note_counts = [(note_type, notes.count(note_type)) for note_type in note_types] # get count of each note length
		return max(note_counts, key=lambda item: item[1])[0] * 2
	elif algorithm == 2:
		return max([note.length for note_set in note_sets for note in note_set])
	elif algorithm == 3:
		return max([note.length for note_set in note_sets for note in note_set]) * 2
	else:
		return 4

