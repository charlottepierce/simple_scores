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

		self.note_batch = pyglet.graphics.Batch() # batch renderer for note blocks

		self.note_sets = note_sets
		self.note_blocks = util.create_note_blocks(self.note_batch, self.note_sets, semibreve_size=250.0)
		self._init_x_locs()

		self.staff_batch = pyglet.graphics.Batch() # batch renderer for staff lines
		self.staff_lines = self._create_staff_lines(self.staff_batch)

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

		result = []
		# Middle and above
		y_pos = self.height / 2
		while y_pos <= self.height:
			result.append(StaffLine(batch, y_pos, self.width))
			y_pos += NoteBlock.HEIGHT
		# Below middle
		y_pos = self.height / 2
		while y_pos >= 0:
			y_pos -= NoteBlock.HEIGHT
			result.append(StaffLine(batch, y_pos, self.width))

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
		self.note_blocks[0].x -= 1
		self._propagate_x_locs()

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

	def _propagate_x_locs(self):
		"""Offset positions of each block with the first.

		Use this so you only have to update the first block excplicitly.

		"""

		for i in range(len(self.note_blocks)):
			note_block = self.note_blocks[i]
			# if first block, ignore
			if i == 0:
				continue

			# not first block - offset position with previous block
			prev = self.note_blocks[i - 1]
			note_block.x = prev.x + prev.width

	def on_draw(self):
		"""Window drawing.

		Clear the window and draw everything assigned to all batch renderers.

		"""

		self.clear()
		self.staff_batch.draw()
		self.note_batch.draw()

