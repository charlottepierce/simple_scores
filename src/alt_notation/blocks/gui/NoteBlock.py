import pyglet

class NoteBlock(pyglet.sprite.Sprite):
	def __init__(self, batch, x=100, y=100, width=100, height=100):
		# build a solid white image for the block
		pattern = pyglet.image.SolidColorImagePattern((255, 255, 255, 255))
		image = pyglet.image.create(width, height, pattern)

		pyglet.sprite.Sprite.__init__(self, image, x, y, batch=batch)

