import pyglet

import gui

class BlockWindow(pyglet.window.Window):
	def __init__(self, width, height):
		pyglet.window.Window.__init__(self, width=width, height=height)

		self.batch = pyglet.graphics.Batch() # batch renderer
		pyglet.clock.schedule_interval(self.update, 1.0/60.0) # call update 60 times a second

		self.note = gui.NoteBlock(self.batch, x=200, y=200, width=100, height=100)

	def update(self, dt):
		# dt = number of seconds that have passed since last update
		print 'Updating game window'
		print 'dt:', dt
		self.note.x += dt

	def on_draw(self):
		self.clear()
		self.batch.draw()

