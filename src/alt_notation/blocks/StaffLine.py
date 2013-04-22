import pyglet

class StaffLine(pyglet.sprite.Sprite):
	HEIGHT = 1

	def __init__(self, batch, y, width, label, color=(215, 196, 196, 50), label_color=(215, 196, 196, 200)):
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
				Default is a light, transparent grey.

		"""

		# build image for the line
		pattern = pyglet.image.SolidColorImagePattern(color)
		image = pyglet.image.create(width, StaffLine.HEIGHT, pattern)

		# create sprite, add to renderer
		pyglet.sprite.Sprite.__init__(self, image, 10, y, batch=batch)

		self.label = pyglet.text.Label(label, font_size=12, x=self.x, y=(self.y + 4), color=label_color)

