class Note:
	def __init__(self, pitch, octave, length, accidental, articulation):
		"""Create a new Note object.

		args
		----
			pitch:
				The pitch of the note.
				One of [a, b, c, d, e, f, g]

			octave:
				The octave of the note.
				Written in Lilyponds version of Helmholtz notation.

			length:
				The length of the note in Lilypond notation.
				i.e., where '1' is a semibreve, '2' is a minim, '8' is a quaver etc.

			accidental:
				Any accidental that should be applied to the note; 'is' sharpens, 'es' flattens.

			articulation:
				Any articulation mark applied to the note.

		"""

		self.pitch = pitch
		self.octave = octave
		self.length = length
		self.accidental = accidental
		self.articulation = articulation

	def __str__(self):
		note_str = self.pitch + self.accidental + self.octave + self.length
		if not self.articulation == '':
			note_str += '-%s' %(self.articulation)

		return note_str

