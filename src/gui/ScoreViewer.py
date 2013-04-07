import Tkinter as tk
import Image, ImageTk

import lilypond as ly

class ScoreViewer:
	def __init__(self, score_file):
		self.root = tk.Tk()
		self.spacing_ref = 4
		self.score_file = score_file
		self.hidden_files = []
		self.viewed = False

	def view(self):
		if self.viewed:
			return

		self.viewed = True

		score_img = ly.typesetting_tools.typeset_score(self.score_file, 'png')
		self.hidden_files.append(score_img)

		tk_score_img = ImageTk.PhotoImage(Image.open(score_img))
		panel = tk.Label(self.root, image=tk_score_img)
		panel.pack()
		self.root.mainloop()
# TODO: find PDF viewer
# TODO: add key bindings/handlers
# TODO: clean up spacing_tools code

