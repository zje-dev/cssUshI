from tkinter import *
import tkinter
from tkinter import ttk
from tkinter import messagebox
import os, sys
from lxml import etree
from io import StringIO, BytesIO
from tkinter import filedialog
from tkinter.colorchooser import *
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
	clazz = [""]
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
		Label(fonnnt,text="tamaño de fuente: ").grid(row=2,column=0)
		Label(fonnnt,text="espacio entre elementos: ").grid(row=3,column=0)
		sc = Scale(fonnnt,from_=0,to=300,orient=HORIZONTAL)
		pd = Scale(fonnnt,from_=0,to=100, orient=HORIZONTAL)
		sc.grid(row=2,column=1,columnspan=4)
		pd.grid(row=3,column=1,columnspan=4)
		self.opciones.add(fonnnt, text="colores", padding=5)
		grupos = Frame(par)
		Label(grupos,text="selecciona el grupo: ").grid(row=0,column=0)
		cass = ttk.Combobox(grupos)
		cass["values"] = self.clazz
		cass.grid(row=0,column=1)
		classNameTF = Entry(grupos)
		classNameTF.grid(row=1,column=1)
		Label(grupos,text="nombre del nuevo grupo: ").grid(row=1,column=0)
		def quiVue ():
			self.clazz.remove(cass.get())
			cass["values"] = self.clazz
			cass.current(0)
		Button(grupos,text="quitar grupo",activebackground="#a60000",bg="red",command=quiVue).grid(row=3,column=0,columnspan=2)
		def addVue ():
			if len(classNameTF.get()) > 0:
				self.clazz.append(classNameTF.get())
				cass["values"] = self.clazz
				cass.current(len(self.clazz) - 1)
			else:
				messagebox.showerror("Error", "Error el grupo no tiene nombre")
		def adGrup ():
			ip = "".join(xmlTree.item(xmlTree.focus())["values"])
			PTFD = etree.fromstring(ip)
			PTFD.set("class",cass.get())
			pi = etree.tostring(PTFD).decode()
			os.chdir(xml[0:xml.rfind("/")+1])
			command = "sed -i \'s|"+ip+"|"+pi+"|g\' "+(xml + " ")[xml.rfind("/")+1:-1]
			print(command)
			os.system(command)
		Button(grupos,text="agregar grupo",command=addVue).grid(row=2,column=0,columnspan=2)
		def sacarDelGrupo ():
			ip = "".join(xmlTree.item(xmlTree.focus())["values"])
			if "class" in ip[0:ip.find(">") + 1]:
				ss = etree.fromstring(ip)
				reovevoer = 'class="'+ss.get("class")+'"'
				ih = ip.replace(reovevoer,'') 
				command = "sed -i \'s|"+ip+"|"+ih+"|g\' "+(xml + " ")[xml.rfind("/")+1:-1]
				os.chdir(xml[0:xml.rfind("/")+1])
				os.system(command)
			else:
				messagebox.showerror("Error", "Error el elemento no es de ningun grupo")
		Button(grupos,text="quitar del grupo",activebackground="#a60000",bg="red",command=sacarDelGrupo).grid(row=5,column=0,columnspan=2)
		self.opciones.add(grupos, text="grupos", padding=5)
		Button(grupos, text="añadir elemento al grupo",command=adGrup).grid(row=4,column=0,columnspan=2)
		def quitCool ():
			ip = "".join(xmlTree.item(xmlTree.focus())["values"])
			if "style" in ip[0:ip.find(">") + 1]:
				ss = etree.fromstring(ip)
				reovevoer = 'style="'+ss.get("style")+'"'
				ih = ip.replace(reovevoer,'') 
				command = "sed -i \'s|"+ip+"|"+ih+"|g\' "+(xml + " ")[xml.rfind("/")+1:-1]
				print(command)
				os.chdir(xml[0:xml.rfind("/")+1])
				os.system(command)
			else:
				messagebox.showerror("Error", "Error el elemento no tiene ningun estilo")
			formaHTML(c, xml)
		Button(fonnnt,text="color de texto", command=colorPick).grid(row=11,column=0)
		Button(fonnnt,text="color de fondo", command=bolorPick).grid(row=10,column=0)
		Button(fonnnt,text="limpiar color", command=bolorPickt).grid(row=11,column=1)
		Button(fonnnt,text="limpiar fondo", command=bolortPick).grid(row=10,column=1)
		Button(fonnnt,text="quitar estilo",activebackground="#a60000",bg="red", command=quitCool).grid(row=12,column=0,columnspan=2)
		f = os.popen("cd "+xml[0:xml.rfind("/")+1]+"; cat "+xml[xml.rfind("/")+1:-1]).read()
		parser = etree.HTMLParser()
		tree = etree.parse(StringIO(f), parser).getroot()
		fz = Scale(par,from_=0,to=400, orient=HORIZONTAL)
		def checkD ():
			ip = "".join(xmlTree.item(xmlTree.focus())["values"])
			print(ip)
			scri = etree.fromstring(ip)
			if "style" in scri.attrib:
				ip = scri.get("style")
			else:
				ip = ""
			#dire.get()
			sass = {}
			sass["color"] = self.textColor[1]
			if self.backColor[1] != None:
				if len(self.backColor[1]) > 1:
					sass["background-color"] = self.backColor[1]
			if sc.get() > 0:
				sass["font-size"] = int(sc.get())
			if pd.get() > 0:
				sass["padding"] = int(pd.get())
			ts = etree.tostring(scri)
			ts = str(ts)[2:str(ts).find(">") + 1]
			scri.set("style",cssWrite(sass))
			os.chdir(xml[0:xml.rfind("/")+1])
			tg = xml + " "
			tj = str(etree.tostring(scri))
			command = "sed -i \'s|"+ts+"|"+tj[2:tj.find(">") + 1]+"|g\' "+tg[xml.rfind("/")+1:-1]
			print(command)
			os.system(command)
			print(command)
			jTT = tj.replace(ts,tj[2:tj.find(">")])[2:-1]
			xmlTree.item(xmlTree.focus(), text=xmlTree.item(xmlTree.focus())["text"], values=tuple([jTT]))
			del(tg)
			del(jTT)
			formaHTML(c, xml)
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
			selected = "".join(xmlTree.item(xmlTree.focus())["values"])
			parOne(self.imap,selected)
		xmlTree.bind("<ButtonPress-1>", preV)
		xmlTree.grid(row=0,column=0)
		hd = xmlTree.insert("", END, text="HTML", values=(str(etree.tostring(tree[1]))[2:-1]))
		def tf (element,xt,pr):
				rl = etree.tostring(element).decode()
				ei = xt.insert(pr, END, text=element.tag, values=tuple([rl]))
				for subEle in element:
					tf(subEle,xt,ei)
		tf(tree[1],xmlTree,hd)
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
		meniu = Menu(self.root)
		self.root.config(menu=meniu)
		def Open ():
			self.openendFile = filedialog.askopenfilename(filetypes=(("documento HTML", "*.html"),("cualquier tipo","*.*")))
			editar(self.openendFile)
		def backUp ():
			if len(self.openendFile) > 0:
				oof = self.openendFile + " "
				comandev = "cp "+oof+" "+os.getcwd()+"/proyectos"+oof[oof.rfind("/"):-1]
				os.system(comandev)
		archivo = Menu(meniu)
		archivo.add_command(label="Abrir", command= Open)
		archivo.add_command(label="Copiar", command= backUp)
		meniu.add_cascade(label="Archivo", menu=archivo)
		try:
			self.root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='src/logo.png'))
		except:
			pass
		self.root.configure(background="#a8a8a8")
		i = 0
		W = self.root.winfo_screenwidth()
		H = self.root.winfo_screenheight()
		i = 0
		def quif ():
			self.root.destroy()
			self.edi.root.destroy()
		self.root.protocol("WM_DELETE_WINDOW",quif)
		def editar (data):
			foor = Frame(self.root, bg="#dbdbdb")
			foor.grid(row=1,column=0)
			if not data == 0:
				data = data + " "
				tyfe = data[data.rfind('.')-1]
				self.root.attributes('-zoomed', True)
				self.cav = Frame(foor,bg="white")
				self.cav.grid(row=0,column=1,sticky="we")
				i = 0
				self.edi = editCanva(self.cav, W, H, data)
				formaHTML(self.cav, data)
		Label(self.root,text="cssUshI por zje 2019").grid(row=29,column=0)
root = Tk()
app = inicio("cssUshI", root, None, Tk)
root.mainloop()