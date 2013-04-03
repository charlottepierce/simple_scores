import sys
import os
import Tkinter
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

def display_score(score_image_file):
	"""
	TODO: Shouldn't be in this file.
	TODO: Check file type, probably change to PDF.
	"""

	root = Tkinter.Tk() # create window

	score = Image.open(score_image_file)
 	root.geometry('%dx%d' % (score.size[0], score.size[1])) # set the size of the image window

	tk_score = ImageTk.PhotoImage(score)
 	label_image = Tkinter.Label(root, image=tk_score) # create label from image
	label_image.place(x=0, y=0, width=score.size[0], height=score.size[1]) # place image on window
	root.title(score_image_file)
 	root.mainloop() # display window until closed

if __name__ == '__main__':
	"""
	TODO: Find PDF viewer.
	"""
	print ' -- Lilypond proportional spacing tool --'

	output_format = 'png'

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
	out_file = '.%s' %(score_file_base) # suffix is added by Lilypond
	ly_command = 'lilypond --silent -o %s --%s %s' %(out_file, output_format, score_file)
	os.system(ly_command)
	out_file += '.%s' %(output_format)
	print 'done (%s).' %(out_file)

	display_score(out_file)


