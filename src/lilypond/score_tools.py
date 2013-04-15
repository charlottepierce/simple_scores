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

	Assumes the Lilypond score is well-formed.

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

	# TODO: add support for articulation position modifiers (i.e., ^ and _)
	# TODO: add support for key signatures
	# TODO: add support for dynamics
	# TODO: add support for clefs
	# TODO: add support for nested slurs
	# TODO: add support for bar checks
	# TODO: add support for relative mode
	# TODO: add support for tempo markings
	# TODO: add support for time signatures

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
			# Articulation and fingering
			articulation = ''
			fingering = ''
			articulation_precursors = [i for i, char in enumerate(note) if char == '-']
			for articulation_precursor in articulation_precursors:
				if note[articulation_precursor - 1] == '-':
					continue # is a tenuto, not articulation precursor

				articulation_mark = note[articulation_precursor + 1]
				if articulation_mark in ['1', '2', '3', '4', '5']:
					fingering = articulation_mark
				else:
					articulation = articulation_mark
			# Slurs
			slur = ''
			if '(' in note:
				slur = '('
			elif ')' in note:
				slur = ')'
			# Ties
			tied = False
			if '~' in note:
				tied = True

			note_objects.append(Note(pitch, octave, length, accidentals, articulation, fingering, slur, tie=tied))

		object_lists.append(note_objects)

	return object_lists

def save_score(note_lists, out_file, articulation=True, fingering=True, ties=True, slurs=True):
	"""Save a score represented as a set of Note object lists.

	args
	----
		note_lists:
			A list of lists
			Each item in the list is an individual set of related notes,
			represented as Note objects.

		out_file:
			The file to save the score in.

		articulation:
			Indicates whether articulation should be included in the saved score.

		fingering:
			Indicates whether fingering should be included in the saved score.

		ties:
			Indicates whether ties should be included in the saved score.

		slurs:
			Indicates whether slurs should be included in the saved score.

	"""

	out = open(out_file, 'w+')
	out.write('\\version \"2.16.2\"\n')
	for note_set in note_lists:
		out.write('{ ')
		for note in note_set:
			out.write('%s ' %(note.create_string(articulation=articulation, fingering=fingering, tie=ties, slur=slurs)))
		out.write('}')
		out.write('\n')

