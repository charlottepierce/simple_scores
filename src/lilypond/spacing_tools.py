import sys
import os

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


if __name__ == '__main__':
	print ' -- Lilypond proportional spacing tool --'

	print 'Using score ... ',
	if len(sys.argv) < 2:
		print "no score given."
		print
		sys.exit(0)

	score_file = sys.argv[1]
	score_file_base = os.path.basename(score_file)
	print '%s (%s)' %(score_file, score_file_base)

	print 'Reading score ... ',
	score_text = open(score_file).read()
	print 'done.'

	print 'Typesetting score ... ',
	out_file = '.%s' %(score_file_base)
	ly_command = 'lilypond -o %s %s' %(out_file, score_file)
	os.system(ly_command)
	print 'done (%s).' %(out_file)

