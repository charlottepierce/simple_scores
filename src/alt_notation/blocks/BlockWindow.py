import pyglet

import block_util as util
import lilypond as ly
from alt_notation.blocks.NoteBlock import NoteBlock

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

		self.batch = pyglet.graphics.Batch() # batch renderer

		self.note_sets = note_sets
		self.note_blocks = util.create_note_blocks(self.batch, self.note_sets, semibreve_size=250.0)

		pyglet.clock.schedule_interval(self.update, 1.0/60.0) # call update 60 times a second

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

		print 'Updating game window'
		print 'dt:', dt

		# update horizontal position of each block
		for i in range(len(self.note_blocks)):
			note_block = self.note_blocks[i]
			# if first block, place at x = 0
			if i == 0:
				note_block.x = BlockWindow.LEFT_MARGIN
				continue

			# not first block - offset position with previous block
			prev = self.note_blocks[i - 1]
			note_block.x = prev.x + prev.width

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

		Clear the window and draw everything assigned to the windows batch renderer.

		"""

		self.clear()
		self.batch.draw()

