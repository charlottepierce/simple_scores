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

def change_score(e, panel, spacing_increase, score_text, spacing_ref):
	if spacing_increase:
		spacing_ref.curr_spacing *= 2
	else:
		spacing_ref.curr_spacing /= 2

	print "Spacing: %d" %(spacing_ref.curr_spacing)

	spaced_score = add_proportional_spacing(score_text, spacing_ref.curr_spacing)
	score_file = '.spaced_score.ly'
	open(score_file, 'w+').write(spaced_score)
	out_file = typeset_score(score_file, 'png')

	img2 = ImageTk.PhotoImage(Image.open(out_file))
	panel.configure(image = img2)
	panel.image = img2

class SpacingRef():
	def __init__(self):
		self.curr_spacing = 1

if __name__ == '__main__':
	"""
	TODO: Find PDF viewer.
	"""
	print ' -- Lilypond proportional spacing tool --'

	output_format = 'png'
	spacing_ref = SpacingRef()

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
	out_file = typeset_score(score_file, output_format)
	print 'done (%s).' %(out_file)

	print 'Creating GUI ... ',
	root = tk.Tk()
	img = ImageTk.PhotoImage(Image.open(out_file))
	panel = tk.Label(root, image=img)
	panel.pack()
	root.bind("i", lambda event: change_score(event, panel, True, score_text, spacing_ref))
	root.bind("d", lambda event: change_score(event, panel, False, score_text, spacing_ref))
	root.mainloop()
	print 'done.'

