import re

def remove_comments(score_file):
	"""Remove the comments from a Lilypond score.

	Assumes the comments are single line, where the comment character is
	the first character in the line.

	args
	----
		score_file:
			The lilypond file to remove the comments from.

	return
	------
		The text of the score file, with comments removed.

	TODO: More complex comment removal.

	"""
	score_text = ''

	with open(score_file) as score:
		for line in score:
			if not line.startswith('%'):
				score_text += line

	return score_text

def find_note_sets(score_text):
	"""Find and return the list of note sets in the score.

	Note sets are a related set of note definitions, found between curly parentheses.
	Currently, it is assumed that all data between curly parentheses
	is a set of note definitions.

	TODO: More complex note set finding.

	args
	----
		score_text:
			The Lilypond score.

	return
	------
		List of note sets in the score.
	"""

	return re.findall(r'{[^}]+}', score_text.replace('\n', ' '))

def create_note_lists(note_sets):
	"""Convert each set in note_sets to a list of notes in that set.

	args
	----
		note_sets:
			List of note collections.

	return
	------
		List where each item is a list of notes found in that note set.

	"""

	return [re.sub(r'[{}]', '', s).strip().split() for s in note_sets]

if __name__ == '__main__':
	score_file = 'scores/Scale.ly'

	score_text = remove_comments(score_file)
	note_sets = find_note_sets(score_text)
	note_lists = create_note_lists(note_sets)

	for n in note_lists:
		print n

