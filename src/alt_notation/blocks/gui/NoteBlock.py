import pyglet

class NoteBlock(pyglet.sprite.Sprite):
	def __init__(self, batch, x=100, y=100, width=100, height=100, color=(255, 255, 255, 255)):
		"""Create a NoteBlock object.

		args
		----
			batch:
				The batch renderer the note block will be drawn by.

			x:
				The x-coordinate of the block.

			y:
				The y-coordinate of the block.

			width:
				The width of the block.

			height:
				The height of the block.

			color:
				The color of the block, as a RGBA tuple.

		"""

		# build an image for the block
		pattern = pyglet.image.SolidColorImagePattern(color)
		image = pyglet.image.create(width, height, pattern)

		# create sprite, add to nominated batch renderer
		pyglet.sprite.Sprite.__init__(self, image, x, y, batch=batch)

