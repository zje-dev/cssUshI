from tkinter import *
import tkinter
from tkinter import ttk
import json
import os, sys
from lxml import etree
from io import StringIO, BytesIO
from tkinter import filedialog
from tkinter.colorchooser import *
from PIL import Image, ImageTk
from json import *
from webbrowser import *
from PIL import *
from src.lib.formaHtml import formaHTML
from src.lib.formaHtml import cssRead
from src.lib.formaHtml import cssWrite
sys.path.append(".dev")
#from devC import dev_mode
class editCanva:
	def __init__ (self,c, w, h, xml):
		par = Tk()
		textColor = "black"
		backColor = ""
		par.title("editar")
		par.geometry("+"+str(w)+"+10")
		canv = Canvas(par, width = w / 6, height = h / 6, background="white")
		canv.grid(row=1,column=0)
		def colorPick ():
			global textColor
			textColor = askcolor()
		Button(par,text="color de texto", command=colorPick).grid(row=3,column=0)
		#Button(par,text="color de fondo", command=self.colorPickBG).grid(row=4,column=0)
		def checkD ():
			ip = "".join(xmlTree.item(xmlTree.focus())["values"])
			if len(ip) > 0:
				global textColor
				sass = cssRead(ip)
				sass["color"] = textColor[1]
				print(cssWrite(sass))
			formaHTML(c, xml, int(h / 1.5), int(w / 1.5))
		Button(par,text="aplicar cambios",command=checkD).grid(row=5,column=0)
		tre = Frame(par, background="black")
		tre.grid(row=6,column=0)
		xmlTree = ttk.Treeview(tre)
		xmlTree.grid(row=0,column=0)
		hd = xmlTree.insert("", END, text="HTML")
		f = os.popen("cd "+xml[0:xml.rfind("/")+1]+"; cat "+xml[xml.rfind("/")+1:-1]).read()
		parser = etree.HTMLParser()
		tree = etree.parse(StringIO(f), parser).getroot()
		for ele in tree[1]:
			if "style" in ele.attrib:
				ei = xmlTree.insert(hd, END, text=ele.tag, values=(ele.get("style")))
			else:
				ei = xmlTree.insert(hd, END, text=ele.tag)
			if ele.tag == "div":
				for subele in ele:
					if "style" in subele.attrib:
						ei = xmlTree.insert(hd, END, text=subele.tag, values=(subele.get("style")))
					else:
						ei = xmlTree.insert(hd, END, text=subele.tag)
class inicio:
	editor = None
	root = None
	tmp = []
	images = []
	newRoot = None
	H = 0
	W = 0
	dir = ""
	v = None
	openendFile = ""
	cav = None
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
						self.cav = Canvas(foor, background="white", width = W / 1.3, height = H / 1.3)
						self.cav.grid(row=0,column=1,sticky="we")
						isHow.destroy()
						i = 0
						for i in range(3):
							coma = None
							b = Button(foor)
							b.grid(row=1,column=i)
						ed = editCanva(self.cav, W, H, data)
						formaHTML(self.cav, data, int(H / 1.5), int(W / 1.5))
					def isCUI ():
						isHow.destroy()
					Button(isHow,text="HTML", command=isHTML).pack(fill=X)
					Button(isHow,text="proyecto", command=isCUI).pack(fill=X)
if len(sys.argv) > 1:
	pass
#	if sys.argv[1] == "-dev_console":
#		dev_mode()
else:
	root = Tk()
	app = inicio("cssUshI", root, ImageTk, Tk)
	root.mainloop()