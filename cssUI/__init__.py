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
						cav = Canvas(foor, background="white", width = W / 1.5, height = H / 1.5)
						cav.grid(row=0,column=1,sticky="we")
						isHow.destroy()
						def zoomIn ():
							cav.config(width = cav.winfo_width() + 25, height = cav.winfo_height() + 35)
							cav.delete("all")
							formaHTML(cav, data, cav.winfo_height(), cav.winfo_width())
						def zoomOu ():
							cav.config(width = cav.winfo_width() - 25, height = cav.winfo_height() - 35)
							cav.delete("all")
							formaHTML(cav, data, cav.winfo_height(), cav.winfo_width())
						i = 0
						for i in range(5):
							coma = None
							if i == 3:
								coma = zoomIn
							if i == 4:
								coma = zoomOu
							b = Button(foor, command=coma)
							b.grid(row=1,column=i)
							if i == 3:
								b.configure(text="+")
							if i == 4:
								b.configure(text="-")
						formaHTML(cav, data, H / 1.5, W / 1.5)
					def isCUI ():
						isHow.destroy()
					Button(isHow,text="HTML", command=isHTML).pack(fill=X)
					Button(isHow,text="proyecto", command=isCUI).pack(fill=X)
root = Tk()
app = inicio("cssUshI", root, ImageTk, Tk)
root.mainloop()
