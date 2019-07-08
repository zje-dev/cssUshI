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
from src.lib.ttkHTML import formaHTML
from src.lib.formaHtml import cssRead
from src.lib.formaHtml import cssWrite
from src.lib.ttkHTML import parOne
class editCanva:
	textColor = [None,"black"]
	backColor = [None,""]
	root = None
	opciones = None
	imap = None
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
		def bolortPick ():
			self.backColor = [None,""]
		self.opciones = ttk.Notebook(par)
		self.opciones.grid(row=8,column=0)
		fonnnt = Frame(par)
		Label(fonnnt,text="la etiqueta: ").grid(row=1,column=0)
		etiqueta = ttk.Combobox(fonnnt)
		etiqueta["values"] = ["span","b","i","sub","sup","h1","h2","h3","h4","h5","h6"]
		etiqueta.grid(row=1,column=1)
		Label(fonnnt,text="tamaño de fuente: ").grid(row=2,column=0)
		sc = Scale(fonnnt,from_=0,to=300,orient=HORIZONTAL)
		sc.grid(row=2,column=1,columnspan=2)
		tipTex = ttk.Combobox(fonnnt)
		tipTex["values"] = ["px","%"]
		Label(fonnnt,text="formato de tamaño: ").grid(row=3,column=0)
		tipTex.grid(row=3,column=1)
		self.opciones.add(fonnnt, text="fuente y etiqueta", padding=5)
		grupos = Frame(par)
		self.opciones.add(grupos, text="grupos", padding=5)
		def quitCool ():
			formaHTML(c, xml, int(h / 1.5), int(w / 1.5))
			ip = "".join(xmlTree.item(xmlTree.focus())["values"]).replace("style"," style")
			scri = etree.fromstring(ip)
			ts = etree.tostring(scri)
			ts = str(ts)[2:str(ts).find(">")].replace(":", ": ")
			if "style" in scri.attrib:
				del(scri.attrib["style"])
			tj = str(etree.tostring(scri))
			command = "sed -i \'s|"+ts.replace(";","; ")+"|"+tj[2:tj.find(">")]+"|g\' "+(xml + " ")[xml.rfind("/")+1:-1]
			os.chdir(xml[0:xml.rfind("/")+1])
			os.system(command)
			formaHTML(c, xml, int(h / 1.5), int(w / 1.5))
			xmlTree.item(xmlTree.focus(), text=xmlTree.item(xmlTree.focus())["text"], values=(tj[2:-1]))
			preV(None)
		Button(par,text="color de texto", command=colorPick).grid(row=3,column=0)
		Button(par,text="color de fondo", command=bolorPick).grid(row=4,column=0)
		Button(par,text="limpiar color", command=bolorPickt).grid(row=3,column=1)
		Button(par,text="limpiar fondo", command=bolortPick).grid(row=4,column=1)
		Button(par,text="quitar estilo",activebackground="#a60000",bg="red", command=quitCool).grid(row=5,column=1)
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
			if sc.get() > 0:
				sass["font-size"] = (sc.get() + tipTex.get())
			sass["color"] = self.textColor[1]
			if self.backColor[1] != None:
				if len(self.backColor[1]) > 1:
					sass["background-color"] = self.backColor[1]
			ts = etree.tostring(scri)
			ts = str(ts)[2:str(ts).find(">")].replace(":", ": ")
			scri.set("style",cssWrite(sass))
			os.chdir(xml[0:xml.rfind("/")+1])
			if len(etiqueta.get()) > 0:
				scri.tag = etiqueta.get()
			tg = xml + " "
			tj = str(etree.tostring(scri))
			command = "sed -i \'s|"+ts.replace(";","; ")+"|"+tj[2:tj.find(">")]+"|g\' "+tg[xml.rfind("/")+1:-1]
			os.system(command)
			print(command)
			jTT = tj.replace(ts.replace(";","; "),tj[2:tj.find(">")])[2:-1]
			if len(etiqueta.get()) > 0:
				command = "sed -i \'s|"+ts[ts.find("</"):-1]+"|"+tj[2:tj.find(">")]+"|g\' "+tg[xml.rfind("/")+1:-1]
				print(command)
			xmlTree.item(xmlTree.focus(), text=xmlTree.item(xmlTree.focus())["text"], values=(jTT))
			del(tg)
			del(jTT)
			formaHTML(c, xml, int(h / 1.5), int(w / 1.5))
			preV(None)
		Button(par,text="aplicar cambios",command=checkD).grid(row=5,column=0)
		ttk.Separator(par,orient="horizontal").grid(row=7,column=0,sticky="we")
		tre = Frame(par, background="black")
		tre.grid(row=6,column=0)
		xmlTree = ttk.Treeview(tre)
		def preV (event):
			if self.imap == None:
				self.imap = Frame(par)
				self.imap.grid(row=6,column=1)
			else:
				self.imap.destroy()
				self.imap = Frame(par)
				self.imap.grid(row=6,column=1)
			selected = "".join(xmlTree.item(xmlTree.focus())["values"]).replace("style"," style")
			parOne(self.imap,selected)
		xmlTree.bind("<ButtonPress-1>", preV)
		xmlTree.grid(row=0,column=0)
		hd = xmlTree.insert("", END, text="HTML", values=(etree.tostring(tree[1]).decode()))
		for ele in tree[1]:
			rl = etree.tostring(ele).decode()
			ei = xmlTree.insert(hd, END, text=ele.tag, values=(rl))
			if ele.tag == "div":
				for subele in ele:
					rl = etree.tostring(subele)
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
					self.root.attributes('-zoomed', True)
		#			self.cav = Canvas(foor, background="white", width = W / 1.3, height = H / 1.3)
					self.cav = Frame(foor,bg="white")
					self.cav.grid(row=0,column=1,sticky="we")
					i = 0
					self.edi = editCanva(self.cav, W, H, data)
					formaHTML(self.cav, data, int(H / 1.5), int(W / 1.5))
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
						formaHTML(self.cav, data)
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
-mejorar el sistema HTML render
"""