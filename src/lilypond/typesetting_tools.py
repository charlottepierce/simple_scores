import os

def typeset_score(score_file, output_format):
	""" Typeset a score with Lilypond.

	Calls the Lilypond compiler in a subprocess.
	The typeset score is saved as a hidden (i.e., dot) file in the current directory.

	args
	----
		score_file:
			The file containing the Lilypond score to typeset.
			Needs to be a full relative path.
		output_format:
			The format in which to save the typeset score.
			Must be a format accepted by the Lilypond engraver (i.e., 'pdf', 'png' or 'ps').

	"""

	score_file_base = os.path.basename(score_file)

	out_file = '%s-typeset' %(score_file_base) # suffix is added by Lilypond
	if not out_file.startswith('.'):
		out_file = '.%s' %(out_file) # make sure file is hidden

	ly_command = 'lilypond --silent -o %s --%s %s' %(out_file, output_format, score_file)
	os.system(ly_command)

	out_file += '.%s' %(output_format) # append file type to output file name

	return out_file

