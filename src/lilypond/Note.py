class Note:
	def __init__(self, pitch, octave, length, accidental, articulation, fingering, slur, tie=False):
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

			tie:
				If the note is tied to the next.

			slur:
				Any slur marking applied to the note.

		"""

		self.pitch = pitch
		self.octave = octave
		self.length = int(length)
		self.accidental = accidental
		self.articulation = articulation
		self.fingering = fingering
		self.tied = tie
		self.slur = slur

	def create_string(self, pitch=True, octave=True, length=True, accidental=True, articulation=True, fingering=True, tie=True, slur=True):
		"""Create a string representing the note.

		args
		----
			pitch:
				Whether to include the pitch definition.

			octave:
				Whether to include the octave definition.

			length:
				Whether to include the note length definition.

			accidental:
				Whether to include any accidentals.

			articulation:
				Whether to include any articulation.

			fingering:
				Whether to include any fingering marks.

			tie:
				Whether to include a tie (if note has one).

			slur:
				Whether to include any slur marks.

		return
		------
			A string representation of the note with the specific elements included.

		"""

		note = ''
		if pitch:
			note += self.pitch
		if accidental:
			note += self.accidental
		if octave:
			note += self.octave
		if length:
			note += str(self.length)
		if fingering:
			if not self.fingering == '':
				note+= '-%s' %(self.fingering)
		if articulation:
			if not self.articulation == '':
				note += '-%s' %(self.articulation)
		if slur:
			if not self.slur == '':
				note += self.slur
		if tie and self.tied:
			note += '~'

		return note

	def __str__(self):
		note_str = self.pitch + self.accidental + self.octave + str(self.length)
		if not self.fingering == '':
			note_str += '-%s' %(self.fingering)
		if not self.articulation == '':
			note_str += '-%s' %(self.articulation)
		if self.tied:
			note_str += '~'

		return note_str

