import os

import Tkinter as tk
import Image, ImageTk

import pyglet

import gui
import lilypond as ly
import alt_notation.blocks as blocks

# TODO: find PDF viewer

class ScoreViewer:
	def __init__(self, score_file):
		"""Create a ScoreViewer object.

		args
		----
			score_file:
				Lilypond file containing the initial score to display.

		"""

		self.hidden_files = []
		self.score_modifier = gui.ScoreModifier(score_file)

		# Prepare for block notation, but do not display yet
		# TODO: dynamically set window height according to score?
		self.block_window = blocks.BlockWindow(width=1000, height=800, note_sets=self.score_modifier.note_sets)

		self.root = tk.Tk()
		self.viewed = False

		# Copy score to hidden tmp file - don't want to accidentally modify original
		self.score_file = '%s.tmp' %(os.path.basename(score_file))
		if not self.score_file.startswith('.'):
			self.score_file = '.%s' %(self.score_file)

		self.hidden_files.append(self.score_file)
		score_text = open(score_file).read()
		open(self.score_file, 'w+').write(score_text)

	def __add_key_bindings(self, panel):
		"""Add all GUI key bindings.

		Should only be called once, before starting the GUI.

		Key bindings:
			b: Toggle visibility of block notation.

			r: Reset score (remove spacing modifications, add all articuation).

			1: Use spacing estimation algorithm 1.
			2: Use spacing estimation algorithm 2.
			3: Use spacing estimation algorithm 3.
			n: Normalise spacing reference using best estimate.
			i: Increase spacing reference.
			d: Decrease spacing reference.

			a: Toggle articulation.
			f: Toggle fingering.

			t: Toggle ties.
			s: Toggle slurs.

			+: Increase score complexity.
			-: Decrease score complexity.

		args
		----
			panel:
				The Tk panel on which the score is displayed.

		"""

		# Window close handler
		self.root.protocol('WM_DELETE_WINDOW', self.__destroy)

		# Key binding to toggle visibility block notation (b).
		self.root.bind('b', lambda event: self.toggle_block_window())
		# Key binding to reset (r) the score.
		self.root.bind('r', lambda event: self.reset_score(event, panel))
		# Key bindings to change the spacing estimation algorithm to 1, 2, or 3
		self.root.bind('1', lambda event: self.change_spacing_algorithm(event, 1))
		self.root.bind('2', lambda event: self.change_spacing_algorithm(event, 2))
		self.root.bind('3', lambda event: self.change_spacing_algorithm(event, 3))
		# Key bindings to increase (i) and decrease (d) the spacing reference,
		# and estimate the best spacing (n)
		self.root.bind('i', lambda event: self.change_spacing(event, True, panel))
		self.root.bind('d', lambda event: self.change_spacing(event, False, panel))
		self.root.bind('n', lambda event: self.normalise_spacing(event, panel))
		# Key binding to toggle articulation (a) and fingering (f).
		self.root.bind('a', lambda event: self.toggle_articulation(event, panel))
		self.root.bind('f', lambda event: self.toggle_fingering(event, panel))
		# Key bindings to toggle ties (t) and slurs (s).
		self.root.bind('t', lambda event: self.toggle_ties(event, panel))
		self.root.bind('s', lambda event: self.toggle_slurs(event, panel))
		# Key bindings to increase (+) and decrease (-) score complexity.
		self.root.bind('+', lambda event: self.change_complexity(event, panel, True))
		self.root.bind('-', lambda event: self.change_complexity(event, panel, False))

	def toggle_block_window(self):
		"""Toggle the visibility of the block notation window."""

		self.block_window.toggle_visibility()
		if self.block_window.visible:
			pyglet.app.run()

	def reset_score(self, e, panel):
		"""Reset the score - remove any spacing modifications and make all elements visible.

		args
		----
			e:
				The key event triggering the spacing change.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.reset_score()

		self.__display_score(score, panel)
		print ' - score reset'

	def change_complexity(self, e, panel, increase):
		"""Change the score complexity.

		args
		----
			e:
				The key event triggering the spacing change.

			panel:
				The GUI panel upon which the score is displayed.

			increase:
				True if the complexity should increase, otherwise false.

		"""

		score = self.score_modifier.change_complexity(increase)

		self.__display_score(score, panel)

		print '- complexity = %d' %(self.score_modifier.complexity_handler.curr_complexity)

	def change_spacing_algorithm(self, e, algorithm):
		"""Change the spacing estimation algorithm.

		args
		----
			e:
				The key event triggering the spacing change.

			algorithm:
				The spacing algorithm to use.
				1: Most frequent note x 2.
				2: Fastest note in score.
				3: Fastest note in score x 2.

		"""

		self.score_modifier.spacing_handler.algorithm = algorithm
		print  '- spacing algorithm = %d' %(self.score_modifier.spacing_handler.algorithm)

	def change_spacing(self, e, increase, panel):
		"""Change the spacing reference of the score currently being viewed.

		Changes the spacing, typesets the newly spaced score, and updates
		the GUI to display the new score.

		args
		----
			e:
				The key event triggering the spacing change.

			increase:
				If true, the spacing reference is multiplied by 2.
				If false, the spacing reference is divided by 2.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.change_spacing(increase)

		self.__display_score(score, panel)

		print '- spacing = %d' %(self.score_modifier.spacing_handler.curr_spacing_ref)

	def normalise_spacing(self, e, panel):
		"""Change the spacing to the best estimate for same-sized bars.

		Changes the spacing, typesets the newly spaced score, and updates
		the GUI to display the new score.

		args
		----
			e:
				The key event triggering the spacing change.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.normalise_spacing()

		self.__display_score(score, panel)

		print '- spacing = %d' %(self.score_modifier.spacing_handler.curr_spacing_ref)

	def toggle_articulation(self, e, panel):
		"""Toggle articulation of the score.

		If articulation is currently visible, remove articulation.
		If articulation can not currently be seen, make it visible.

		args
		----
			e:
				The key event triggering the articulation toggle.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.toggle_articulation()

		self.__display_score(score, panel)

		print '- articulation = %s' %(str(self.score_modifier.articulation_handler.articulation_on))

	def toggle_fingering(self, e, panel):
		"""Toggle display of fingering marks on the score.

		If fingering is currently visible, remove it.
		If fingering can not currently be seen, make it visible.

		args
		----
			e:
				The key event triggering the articulation toggle.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.toggle_fingering()

		self.__display_score(score, panel)

		print '- fingering = %s' %(str(self.score_modifier.articulation_handler.fingering_on))

	def toggle_ties(self, e, panel):
		"""Toggle display of ties on the score.

		If ties are currently visible, remove them.
		If ties can not currently be seen, make them visible.

		args
		----
			e:
				The key event triggering the articulation toggle.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.toggle_ties()

		self.__display_score(score, panel)

		print '- ties = %s' %(str(self.score_modifier.joins_handler.ties_on))

	def toggle_slurs(self, e, panel):
		"""Toggle display of slurs on the score.

		If slurs are currently visible, remove them.
		If slurs can not currently be seen, make them visible.

		args
		----
			e:
				The key event triggering the articulation toggle.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		score = self.score_modifier.toggle_slurs()

		self.__display_score(score, panel)

		print '- slurs = %s' %(str(self.score_modifier.joins_handler.slurs_on))

	def __display_score(self, score, panel):
		"""Replace the current score being displayed.

		args
		----
			score_img:
				The score to display.

			panel:
				The GUI panel upon which the score is displayed.

		"""

		if score not in self.hidden_files:
			self.hidden_files.append(score)

		score_img = ImageTk.PhotoImage(Image.open(score))
		panel.configure(image=score_img)
		panel.image = score_img

	def view(self):
		"""Start the ScoreViewer.

		Can only be called once (subsequent calls will not be executed).

		Applies the current spacing level to the given input score, adds keybindings
		for changing the score appearance, and displays the GUI.

		"""

		if self.viewed:
			return

		self.viewed = True

		# Typeset score
		score_img = self.score_modifier.typeset_score()
		self.hidden_files.append(score_img)

		# Create and add GUI image element
		tk_score_img = ImageTk.PhotoImage(Image.open(score_img))
		panel = tk.Label(self.root, image=tk_score_img)
		panel.pack()

		# Add key bindings and view GUI
		self.__add_key_bindings(panel)
		self.root.mainloop()

	def __destroy(self):
		"""Clean up all hidden files and close the GUI.

		Assumes the GUI has been closed (or triggered to close).

		"""

		print 'Closing GUI ... '

		for file in self.hidden_files:
			if os.path.isfile(file):
				os.remove(file)

		self.root.destroy()

