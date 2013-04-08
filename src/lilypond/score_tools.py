import re

from Note import Note

# TODO: update for relative pitches

def _remove_comments(score_file):
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

def _find_note_sets(score_text):
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

def _create_note_lists(note_sets):
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

def create_note_objects(score_file):
	"""Convert a Lilypond score into a list of Note objects.

	args
	----
		score_file:
			The Lilypond score to read and convert.

	return
	------
		List of lists.
		Each item in the list is an individual set of related notes,
		represented as Note objects.

	"""

	# TODO: update for articulation

	note_lists = _create_note_lists(_find_note_sets(_remove_comments(score_file)))

	object_lists = []
	for note_list in note_lists:
		note_objects = []
		# Convert each note
		for note in note_list:
			# Pitch
			pitch = note[0] # pitch is always the first thing
			# Octave
			octave = '' # no octave
			if '\'' in note:
				octave = note.count('\'') * '\'' # higher octave
			elif ',' in note:
				octave = note.count(',') * ',' # lower octave
			# Length
			digits = re.findall(r'\d+', note)
			if len(digits) > 0:
				length = digits[0] # assume first not found in note string is the length
			# Accidentals
			accidentals = ''
			if 'es' in note:
				accidentals = note.count('es') * 'es' # flattened
			elif 'is' in note:
				accidentals = note.count('is') * 'is' # sharpened

			note_objects.append(Note(pitch, octave, length, accidentals))

		object_lists.append(note_objects)

	return object_lists

if __name__ == '__main__':
	score_file = 'scores/Scale.ly'

	note_lists = create_note_objects(score_file)

	for note_list in note_lists:
		for note in note_list:
			print note,
		print
