import pyglet

class StaffLine(pyglet.sprite.Sprite):
	HEIGHT = 1

	def __init__(self, batch, y, width, color=(215, 196, 196, 50)):
		"""Create a new StaffLine object.

		x is assumed to be zero.

		args
		----
			batch:
				The batch renderer the line will be drawn by.

			y:
				The y-coordinate of the line.

			width:
				The width of the line.
				Assumedly, would be the width of the screen.

			color:
				The color of the line, as a RGBA tuple.

		"""

		# build image for the line
		pattern = pyglet.image.SolidColorImagePattern(color)
		image = pyglet.image.create(width, StaffLine.HEIGHT, pattern)

		# create sprite, add to renderer
		pyglet.sprite.Sprite.__init__(self, image, 0, y, batch=batch)

