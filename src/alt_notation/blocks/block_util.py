from NoteBlock import NoteBlock

def create_note_blocks(batch, note_sets, semibreve_size=100.0):
	"""Convert note sets to note blocks.

	Adjusts the size of each note block according to the reference size
	for a semibreve.

	Does not set the location of the note blocks.

	args
	----
		batch:
			The batch renderer each note block should use.

		note_sets:
			List of lists.
			Each item in the list should be an individual set of related notes,
			represented as Note objects.

		semibreve_size:
			The size of a semibreve, in pixels.
			Sizes of other note lengths will be calculated from this reference.

	return
	------
		List of notes.
		Invisible (i.e., black) 'break' blocks are placed between individual note sets.

	"""

	result = []
	for note_set in note_sets:
		for note in note_set:
			note_width = int(semibreve_size / float(note.length))
			result.append(NoteBlock(batch, note, width=note_width))

		# create crotchet-sized invisible 'break' block between note sets
		break_width = int(semibreve_size / 4.0)
		result.append(NoteBlock(batch, None, width=break_width, color=(0, 0, 0, 0)))

	return result

# TODO: make aware of key
def pitch_difference(prev_note, next_note):
	"""Calculate the pitch difference moving between two notes.

	For example, if prev_note = C, and next_note is the B below,
	pitch difference = -1.

	If prev_note = C, and next_note is the B above, pitch
	difference = 6.

	If prev_note = C and next_note is C sharp, pitch difference = 0.5.

	args
	----
		prev_note:
			 The note to move from.

		next_note:
			The note to move to.

	return
	------
		The pitch difference between the two notes.

	"""

	# Check note isn't invisible break block
	if next_note.note == None:
		return 0

	pitches = ('c', 'd', 'e', 'f', 'g', 'a', 'b')
	octave_diff = 7
	accidental_diff = 0.5

	prev_index = pitches.index(prev_note.note.pitch)
	next_index = pitches.index(next_note.note.pitch)

	pitch_diff = next_index - prev_index

	prev_octave = prev_note.note.octave
	next_octave = next_note.note.octave

	# different octaves, account for difference
	# one octave is 'blank'
	if prev_octave == '':
		if '\'' in next_octave:
			pitch_diff += (octave_diff * len(next_octave)) # next octave is higher
		elif ',' in next_octave:
			pitch_diff += (-1 * octave_diff * len(next_octave)) # next octave is lower
	elif next_octave == '':
		if '\'' in prev_octave:
			pitch_diff += (-1 * octave_diff * len(prev_octave)) # previous octave was higher
		elif ',' in prev_octave:
			pitch_diff += (octave_diff * len(prev_octave)) # previous octave was lower

	# both are 'positive' octaves
	if ('\'' in prev_octave) and ('\'' in next_octave):
		pitch_diff += (octave_diff * (len(next_octave) - len(prev_octave)))
	# both are 'negative' octaves
	if (',' in prev_octave) and (',' in next_octave):
		pitch_diff += (octave_diff * (len(prev_octave) - len(next_octave)))

	# previous octave is negative, next is positive
	if (',' in prev_octave) and ('\'' in next_octave):
		pitch_diff += (octave_diff * (len(prev_octave) + len(next_octave)))
	# previous octave is positive, next is negative
	if ('\'' in prev_octave) and (',' in next_octave):
		pitch_diff += (-1 * octave_diff * (len(prev_octave) + len(next_octave)))

	# account for accidentals
	prev_acc = prev_note.note.accidental
	next_acc = next_note.note.accidental

	# previous note is sharp
	if ('is' in prev_acc):
		pitch_diff -= accidental_diff * prev_acc.count('is')
	# previous note is flat
	elif ('es' in prev_acc):
		pitch_diff += accidental_diff * prev_acc.count('es')
	# next note is sharp
	if ('is' in next_acc):
		pitch_diff += accidental_diff * next_acc.count('is')
	# next note is flat
	if ('es' in next_acc):
		pitch_diff -= accidental_diff * next_acc.count('es')

	return pitch_diff

