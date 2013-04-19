import pyglet

import lilypond as ly
from alt_notation.blocks.NoteBlock import NoteBlock

class BlockWindow(pyglet.window.Window):
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

	def on_draw(self):
		"""Window drawing.

		Clear the window and draw everything assigned to the windows batch renderer.

		"""

		self.clear()
		self.batch.draw()

