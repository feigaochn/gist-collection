from Tkinter import *

class ParallelPanedWindows(PanedWindow):
	
	collectionOfPanedsWindows = {}
	
	def __init__(self, master, tag= 'default', **kargs):
		
		PanedWindow.__init__(self, master, **kargs)
		
		self.other_paneds_windows = []
		
		if tag in self.collectionOfPanedsWindows:
			for pwindow in self.collectionOfPanedsWindows[tag]:
				self.other_paneds_windows.append(pwindow)
				pwindow.other_paneds_windows.append(self)
				
			self.collectionOfPanedsWindows[tag].append(self)
		else:
			self.collectionOfPanedsWindows[tag] = [self]
				
		
		
		self.bind('<Button-1>', self.sash_mark)
		self.bind('<B1-Motion>', self.sash_dragto)
		
		
	def sash_mark(self,event):
		identity = self.identify(event.x, event.y)

		if len(identity) ==2:
			index = identity[0]
			self.marked=index
		else:
			self.marked = None

	def sash_dragto(self,event):
		if self.marked != None:
			for pwindow in self.other_paneds_windows:
				pwindow.sash_place(self.marked, event.x, event.y)

def test():
	root = Tk()
	m1 = ParallelPanedWindows(root, bd=1, orient=VERTICAL,sashwidth=2,sashrelief=RIDGE)
	m1.place(x=30,y=30)

	top1 = Label(m1, text="top pane1")
	m1.add(top1)

	bottom1 = Label(m1, text="bottom pane1")
	m1.add(bottom1)

	m2 = ParallelPanedWindows(root, bd=1, orient=VERTICAL,sashwidth=2,sashrelief=RIDGE)
	m2.place( x=30, y =130)

	top2 = Label(m2, text="top pane2")
	m2.add(top2)

	bottom2 = Label(m2, text="bottom pane2")
	m2.add(bottom2)

	root.mainloop()

if __name__ == '__main__':
	test()

