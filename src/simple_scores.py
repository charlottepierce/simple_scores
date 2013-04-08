import sys

import gui

if __name__ == '__main__':
	print ' -- Simple Scores -- '

	if len(sys.argv) < 2:
		print "No score given."
		print
		sys.exit(0)

	print 'Using score ... ',
	score_file = sys.argv[1]
	print score_file

	print 'Creating score viewer ... ',
 	score_viewer = gui.ScoreViewer(score_file)
	print 'done.'

	print 'Opening score viewer ... '
	score_viewer.view()

