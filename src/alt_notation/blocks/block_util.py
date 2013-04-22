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
			result.append(NoteBlock(batch, width=note_width))

		# create crotchet-sized invisible 'break' block between note sets
		break_width = int(semibreve_size / 4.0)
		result.append(NoteBlock(batch, width=break_width, color=(0, 0, 0, 0)))

	return result

