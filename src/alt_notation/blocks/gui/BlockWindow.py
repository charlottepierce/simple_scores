import pyglet

import gui

class BlockWindow(pyglet.window.Window):
	def __init__(self, width, height):
		"""Create a BlockWindow object.

		The window will update itself 60 times a second.

		args
		----
			width:
				The initial width of the window.

			height:
				The initial height of the window.
		"""

		pyglet.window.Window.__init__(self, width=width, height=height)

		self.batch = pyglet.graphics.Batch() # batch renderer
		pyglet.clock.schedule_interval(self.update, 1.0/60.0) # call update 60 times a second

		self.note = gui.NoteBlock(self.batch, x=200, y=200, width=100, height=100, color=(255, 255, 255, 150))

	def update(self, dt):
		"""Update the window.

		args
		----
			dt:
				The number of seconds that have passed since the last update.
		"""

		print 'Updating game window'
		print 'dt:', dt
		self.note.x += dt

	def on_draw(self):
		"""Window drawing.

		Clear the window and draw everything assigned to the windows batch renderer.

		"""
		self.clear()
		self.batch.draw()

