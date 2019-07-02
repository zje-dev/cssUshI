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
from PIL import *
from src.lib.formaHtml import formaHTML
from src.lib.formaHtml import cssRead
from src.lib.formaHtml import cssWrite
class editCanva:
	textColor = [None,"black"]
	backColor = [None,""]
	root = None
	def __init__ (self,c, w, h, xml):
		par = Tk()
		par.title("editar")
		def nq():
			pass
		par.protocol("WM_DELETE_WINDOW",nq)
		par.geometry("+"+str(int(w / 2))+"+10")
		def colorPick ():
			self.textColor = list(askcolor())
		def bolorPick ():
			self.backColor = list(askcolor())
		def bolorPickt ():
			self.textColor = [None,"#000000"]
		Label(par,text="tamaño").grid(row=8,column=0,columnspan=2)
		tipoDeTama = ttk.Combobox(par)
		tipoDeTama["values"] = ["tamaño de fuente","ancho","alto"]
		tipoDeTama.grid(row=9,column=0,columnspan=1)
		tipoDemo = ttk.Combobox(par)
		tipoDemo["values"] = ["px (pixeles)","% (porcentaje)"]
		tipoDemo.grid(row=9,column=1,columnspan=2)
		tamano = Scale(par,from_=0,to=300,orient="horizontal")
		tamano.grid(row=10,column=0,columnspan=2, sticky=W+E)
		Label(par, text="fijar directamente el tamaño").grid(row=11,column = 0,columnspan=2)
		dire = Entry(par)
		dire.grid(row=12,column=0,columnspan=2)
		Button(par,text="color de texto", command=colorPick).grid(row=3,column=0)
		Button(par,text="color de fondo", command=bolorPick).grid(row=4,column=0)
		Button(par,text="limpiar color", command=bolorPickt).grid(row=3,column=1)
		Button(par,text="limpiar fondo", command=bolorPickt).grid(row=4,column=1)
		f = os.popen("cd "+xml[0:xml.rfind("/")+1]+"; cat "+xml[xml.rfind("/")+1:-1]).read()
		parser = etree.HTMLParser()
		tree = etree.parse(StringIO(f), parser).getroot()
		fz = Scale(par,from_=0,to=400, orient=HORIZONTAL)
		def checkD ():
			ip = "".join(xmlTree.item(xmlTree.focus())["values"]).replace("style"," style")
			scri = etree.fromstring(ip)
			if "style" in scri.attrib:
				ip = scri.get("style")
			else:
				ip = ""
			#dire.get()
			sass = {}
			sass["color"] = self.textColor[1]
			if len(self.backColor[1]) > 1:
				sass["background-color"] = self.backColor[1]
			ts = etree.tostring(scri)
			ts = str(ts)[2:str(ts).find(">")].replace(":", ": ")
			scri.set("style",cssWrite(sass))
			os.chdir(xml[0:xml.rfind("/")+1])
			tg = xml + " "
			tj = str(etree.tostring(scri))
			command = "sed -i \'s|"+ts.replace("background-color"," background-color")+"|"+tj[2:tj.find(">")]+"|g\' "+tg[xml.rfind("/")+1:-1]
			os.system(command)
			jTT = tj.replace(ts.replace("background-color"," background-color"),tj[2:tj.find(">")])[2:-1]
			xmlTree.item(xmlTree.focus(), text=xmlTree.item(xmlTree.focus())["text"], values=(jTT))
			del(tg)
			del(jTT)
			formaHTML(c, xml, int(h / 1.5), int(w / 1.5))
		Button(par,text="aplicar cambios",command=checkD).grid(row=5,column=0)
		ttk.Separator(par,orient="horizontal").grid(row=7,column=0,sticky="we")
		tre = Frame(par, background="black")
		tre.grid(row=6,column=0)
		xmlTree = ttk.Treeview(tre)
		xmlTree.grid(row=0,column=0)
		hd = xmlTree.insert("", END, text="HTML", values=(etree.tostring(tree[1]).decode()))
		for ele in tree[1]:
			rl = etree.tostring(ele).decode()
			ei = xmlTree.insert(hd, END, text=ele.tag, values=(rl))	
			if ele.tag == "div":
				for subele in ele:
					rl = etree.tostring(subele).decode()
					ei = xmlTree.insert(hd, END, text=subele.tag, values=(rl))
		self.root = par
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
	edi = None
	def __init__ (self, name, master, tk, base):
		self.root = master
		self.root.title(name)
		self.root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='src/img/logo.png'))
		self.root.configure(background="#a8a8a8")
		i = 0
		W = self.root.winfo_screenwidth()
		H = self.root.winfo_screenheight()
		for _ in range(2):
			self.tmp.append(Button(self.root))
			filex = "src/img/i"+str(i)+".png"
			self.images.append(tk.PhotoImage(Image.open(filex)))
			i += 1
		i = 0
		def quif ():
			self.root.destroy()
			self.edi.root.destroy()
		self.root.protocol("WM_DELETE_WINDOW",quif)
		def Open ():
			self.openendFile = filedialog.askopenfilename(filetypes=(("proyecto cssUshI","*.cui"),("documento HTML", "*.html"),("cualquier tipo","*.*")))
			editar(self.openendFile)
		def backUp ():
			if len(self.openendFile) > 0:
				oof = self.openendFile + " "
				comandev = "cp "+oof+" "+os.getcwd()+"/proyectos"+oof[oof.rfind("/"):-1]
				os.system(comandev)
		def organizar (arr, i):
			for e in arr:
				filex = "src/img/i"+str(i)+".png"
				e.grid(row=0,column=i)
				e.configure(image=self.images[i])
				if i == 0:
					e.configure(command=Open)
				if i == 1:
					e.configure(command=backUp)
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
						self.edi = editCanva(self.cav, W, H, data)
						formaHTML(self.cav, data, int(H / 1.5), int(W / 1.5))
					def isCUI ():
						isHow.destroy()
					Button(isHow,text="HTML", command=isHTML).pack(fill=X)
					Button(isHow,text="proyecto", command=isCUI).pack(fill=X)
		Label(self.root,text="cssUshI por zje 2019").grid(row=29,column=0)
root = Tk()
app = inicio("cssUshI", root, ImageTk, Tk)
root.mainloop()
"""
TODO
-hacer una lista con cada elemento del HTML para usar el index para cambiar el texto
-mejorar el sistema HTML render
"""