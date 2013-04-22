import pyglet

import block_util as util
import lilypond as ly
from NoteBlock import NoteBlock
from StaffLine import StaffLine

class BlockWindow(pyglet.window.Window):
	LEFT_MARGIN = 50 # empty space to leave on the left

	def __init__(self, width, height, note_sets):
		"""Create a BlockWindow object.

		The window is invisible by default.
		The window will update itself 60 times a second.

		args
		----
			width:
				The initial width of the window.

			height:
				The initial height of the window.

			note_sets:
				List of lists.
				Each item in the list should be an individual set of related notes,
				represented as Note objects.

		"""

		pyglet.window.Window.__init__(self, width=width, height=height, visible=False)

		# create note blocks and set up to draw
		self.note_batch = pyglet.graphics.Batch() # batch renderer for note blocks
		self.note_sets = note_sets
		self.note_blocks = util.create_note_blocks(self.note_batch, self.note_sets, semibreve_size=250.0)
		self._init_x_locs()

		# create staff lines, set up to draw
		self.staff_batch = pyglet.graphics.Batch() # batch renderer for staff lines
		self.staff_lines = self._create_staff_lines(self.staff_batch)

		# create left margin line
		pattern = pyglet.image.SolidColorImagePattern((215, 196, 196, 200))
		image = pyglet.image.create(1, self.height, pattern)
		self.left_margin = pyglet.sprite.Sprite(image, BlockWindow.LEFT_MARGIN, 0)

		pyglet.clock.schedule_interval(self.update, 1.0/60.0) # call update 60 times a second

	def _init_x_locs(self):
		"""Initialise the x locations for each note block."""

		for i in range(len(self.note_blocks)):
			note_block = self.note_blocks[i]
			# if first block, place at the left margin
			if i == 0:
				note_block.x = BlockWindow.LEFT_MARGIN
				continue

			# not first block - offset position with previous block
			prev = self.note_blocks[i - 1]
			note_block.x = prev.x + prev.width

	def _create_staff_lines(self, batch):
		"""Create the staff lines for the score."""

		pitches = ('c', 'd', 'e', 'f', 'g', 'a', 'b')

		result = []
		# Middle and above
		y_pos = self.height / 2
		pitch = pitches.index(self.note_blocks[0].note.pitch) # first pitch
		while y_pos <= self.height:
			result.append(StaffLine(batch, y_pos, self.width, pitches[pitch]))
			y_pos += NoteBlock.HEIGHT
			pitch += 1
			if pitch >= len(pitches):
				pitch = 0
		# Below middle
		y_pos = self.height / 2
		pitch = pitches.index(self.note_blocks[0].note.pitch) - 1 # first pitch - 1
		if pitch < 0:
			pitch = len(pitches) - 1
		while y_pos >= 0:
			y_pos -= NoteBlock.HEIGHT
			result.append(StaffLine(batch, y_pos, self.width, pitches[pitch]))
			pitch -= 1
			if pitch < 0:
				pitch = len(pitches) - 1

		return result

	def toggle_visibility(self):
		"""Toggle the visibility of the block window.

		If invisible, display.
		If visible, hide.

		"""

		self.set_visible(not self.visible)

	def update(self, dt):
		"""Update the window.

		args
		----
			dt:
				The number of seconds that have passed since the last update.
		"""

		# update horizontal position of each block
		x_change = 1

		# apply horizontal change to all notes
		for note_block in self.note_blocks:
			note_block.x -= x_change

		# change widths
		for note_block in self.note_blocks:
			if note_block.note == None:
				continue

			if note_block.x < BlockWindow.LEFT_MARGIN:
				if note_block.width > x_change:
					# apply the x change to the width, rather than the location
					note_block.x += x_change
					new_width = note_block.width - x_change
					# generate and apply new sprite image
					pattern = pyglet.image.SolidColorImagePattern((255, 255, 255, 255))
					image = pyglet.image.create(new_width, NoteBlock.HEIGHT, pattern)
					note_block.image = image
				else:
					note_block.visible = False

		# update vertical position of each block
		for i in range(len(self.note_blocks)):
			note_block = self.note_blocks[i]
			# if first block, place in vertical centre
			if i == 0:
				note_block.y = self.height / 2
				continue

			# not first block - offset position with previous block
			prev_block = self.note_blocks[i - 1]
			if prev_block.note == None:
				prev_block = self.note_blocks[i - 2]

			pitch_diff = util.pitch_difference(prev_block, note_block)
			note_block.y = prev_block.y + (pitch_diff * NoteBlock.HEIGHT)

	def on_draw(self):
		"""Window drawing.

		Clear the window and draw everything assigned to all batch renderers.

		"""

		self.clear()

		self.left_margin.draw()

		for line in self.staff_lines:
			line.label.draw()

		self.staff_batch.draw()
		self.note_batch.draw()

