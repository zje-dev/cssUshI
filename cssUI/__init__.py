from tkinter import *
import tkinter
import json
import os, sys
from tkinter import filedialog
from PIL import Image, ImageTk
from json import *
from webbrowser import *
from PIL import *
from src.lib.formaHtml import formaHTML
sys.path.append(".dev")
from devC import dev_mode
class inicio:
	root = None
	tmp = []
	images = []
	newRoot = None
	H = 0
	W = 0
	dir = ""
	v = None
	openendFile = ""
	def __init__ (self, name, master, tk, base):
		self.root = master
		self.root.title(name)
		self.root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='src/img/logo.png'))
		self.root.configure(background="#a8a8a8")
		i = 0
		W = self.root.winfo_screenwidth()
		H = self.root.winfo_screenheight()
		for _ in range(5):
			self.tmp.append(Button(self.root))
			filex = "src/img/i"+str(i)+".png"
			self.images.append(tk.PhotoImage(Image.open(filex)))
			i += 1
		i = 0
		def Open ():
			self.openendFile = filedialog.askopenfilename(filetypes=(("proyecto cssUshI","*.cui"),("documento HTML", "*.html"),("cualquier tipo","*.*")))
			editar(self.openendFile)
		def newF ():
			if self.newRoot is None:
				self.newRoot = base()
				def quit ():
					self.newRoot.destroy()
					self.newRoot = None
				self.newRoot.protocol('WM_DELETE_WINDOW', quit)
				self.newRoot.title(" crear proyecto  ")
				self.newRoot.resizable(False, False)
				Label(self.newRoot, text="nombre del proyecto").pack()
				self.v = Entry(self.newRoot)
				self.v.pack()
				Label(self.newRoot, text="donde se debe poner el proyecto").pack()
				def openDir ():
					#global dir
					self.dir = filedialog.askdirectory()
				def crea():
					os.chdir(self.dir)
					os.system("touch "+self.v.get()+".cui")
					quit()
					editar(0)
				Button(self.newRoot, command=openDir, text="selecciona una carpeta").pack()
				Button(self.newRoot, command=crea, text="crear").pack()
		def organizar (arr, i):
			for e in arr:
				filex = "src/img/i"+str(i)+".png"
				e.grid(row=0,column=i+2)
				e.configure(image=self.images[i])
				if i == 0:
					e.configure(command=newF)
				elif i == 4:
					e.configure(command=Open)
				i += 1
		organizar(self.tmp, i)
		def editar (data):
			foor = Frame(self.root, bg="#dbdbdb")
			foor.grid(row=1,column=0)
			if not data == 0:
				data = data + " "
				tyfe = data[data.rfind('.'): -1]
				if tyfe == ".cui":
					render = Canvas(foor, background="white")
					render.grid(row=0,column=1,sticky="we")
				elif type == ".html":
					pass
				else:
					isHow = base()
					isHow.title(" ")
					Label(isHow,text="que tipo de archivo representa?").pack()
					def isHTML ():
						self.root.attributes('-zoomed', True)
						cav = Canvas(foor, background="white", width = W / 1.3, height = H / 1.3)
						cav.grid(row=0,column=1,sticky="we")
						isHow.destroy()
						i = 0
						for i in range(3):
							coma = None
							b = Button(foor)
							b.grid(row=1,column=i)
						formaHTML(cav, data, int(H / 1.5), int(W / 1.5))
						Xm =  Scrollbar(foor, orient="horizontal", command=cav.xview)
						Xm.grid(row=1,column=1,sticky="ew")
						Ym =  Scrollbar(foor, orient="vertical", command=cav.yview)
						Ym.grid(row=0,column=2,sticky="ns")
						cav.configure(yscrollcommand=Ym.set, xscrollcommand=Xm.set)
						cav.configure(scrollregion=(0,0,0,1000))
					def isCUI ():
						isHow.destroy()
					Button(isHow,text="HTML", command=isHTML).pack(fill=X)
					Button(isHow,text="proyecto", command=isCUI).pack(fill=X)
if len(sys.argv) > 1:
	if sys.argv[1] == "-dev_console":
		dev_mode()
else:
	root = Tk()
	app = inicio("cssUshI", root, ImageTk, Tk)
	root.mainloop()
