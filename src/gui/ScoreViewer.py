import Tkinter as tk
import Image, ImageTk

import gui
import lilypond as ly

# TODO: find PDF viewer
# TODO: add key bindings/handlers
# TODO: clean up spacing_tools code

class ScoreViewer:
	def __init__(self, score_file, spacing_ref=1):
		"""Create a ScoreViewer object.

		args
		----
			score_file:
				Lilypond file containing the initial score to display.

			spacing_ref:
				Initial spacing reference.

		"""

		self.root = tk.Tk()
		self.spacing_ref = 4
		self.score_file = score_file
		self.hidden_files = []
		self.viewed = False
		self.spacing_handler = gui.SpacingHandler(spacing_ref)

	def __add_key_bindings(self, panel):
		"""Add all GUI key bindings.

		Should only be called once, before starting the GUI.

		Key bindings:
			i: Increase spacing reference.
			d: Decrease spacing reference.

		args
		----
			panel:
				The Tk panel on which the score is displayed.

		"""

		# Key bindings to increase (i) and decrease (d) the spacing reference
		self.root.bind('i', lambda event: self.__change_spacing(event, True, panel))
		self.root.bind('d', lambda event: self.__change_spacing(event, False, panel))

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
		score_img = ly.typesetting_tools.typeset_score(self.score_file, 'png')
		self.hidden_files.append(score_img)

		# Create and add GUI image element
		tk_score_img = ImageTk.PhotoImage(Image.open(score_img))
		panel = tk.Label(self.root, image=tk_score_img)
		panel.pack()

		# Add key bindings and view GUI
		self.__add_key_bindings(panel)
		self.root.mainloop()

	def __change_spacing(self, e, increase, panel):
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

		# Change spacing, add new score image to hidden file list
		spaced_score = self.spacing_handler.change_spacing(increase, self.score_file)
		if spaced_score not in self.hidden_files: self.hidden_files.append(spaced_score)

		# Add new score image to GUI
		spaced_score_img = ImageTk.PhotoImage(Image.open(spaced_score))
		panel.configure(image=spaced_score_img)
		panel.image = spaced_score_img

		print '- spacing = %d' %(self.spacing_handler.curr_spacing_ref)

