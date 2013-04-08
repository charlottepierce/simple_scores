class Note:
	def __init__(self, pitch, octave, length):
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

		"""

		self.pitch = pitch
		self.octave = octave
		self.length = length

	def __str__(self):
		return self.pitch + self.octave + self.length

