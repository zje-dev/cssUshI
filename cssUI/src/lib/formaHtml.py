#!/usr/bin/python
from tkinter import *
import os
from lxml import etree
from io import StringIO, BytesIO
from tkinter import filedialog
from tkinter.colorchooser import *
xp = 0
yp = 0
textag = ["span","b","i","sub","sup","h1","h2","h3","h4","h5","h6"]
def sizeFormat (s, w):
	z = 0
	if "px" in s:
		z = float(s.replace("px", ""))
	elif "%" in s:
		z = w / (110 / float(s[0:-1]))
	else:
		z = float(s)
	return int(z)
class text:
	align = NW
	element = None
	bg = None
	CSS = {}
	fonZise = 0
	texType = "normal"
	text = ""
	color = "black"
	background_color = ""
	padding = 0
	def __init__(self, parent, x, y, c, w, h, t, a):
		self.text = parent.text
		def fz (me, par):
			if par.tag == "h6":
				me.fonZise = 7
			elif par.tag == "h5":
				me.fonZise = 8
			elif par.tag == "h4":
				me.fonZise = 10
			elif par.tag == "h3":
				me.fonZise = 14
			elif par.tag == "h2":
				me.fonZise = 18
			elif par.tag == "h1":
				me.fonZise = 22
			else:
				me.fonZise = 14
		fz(self, parent)
		if "style" in parent.attrib:
			self.CSS = cssRead(parent.get("style").replace(" ",""))
			if "padding" in parent.get("style"):
				self.padding = sizeFormat(self.CSS["padding"], w)
			if "font-size" in parent.get("style"):
				self.fonZise = sizeFormat(self.CSS["font-size"], w)
			if "background-color" in parent.get("style"):
				self.background_color = self.CSS["background-color"]
				if self.background_color != " ":
					self.bg = c.create_rectangle(x, y, len(self.text) * self.fonZise, y + (self.fonZise * (1.5 + (self.padding * 0.14))), fill=self.background_color, outline="")
		if parent.tag == "b":
			self.texType = "bold"
		if len(self.CSS) > 0:
			self.color = self.CSS["color"].replace(" ","")
		self.color.replace(" ","")
		self.element = c.create_text(x + self.padding, y + self.padding, text=parent.text, anchor=self.align, fill=self.color, font=("Arial", self.fonZise, self.texType))
		if parent.tag == "sup":
			c.coords(self.element, x + self.padding, y + self.padding + 10)
		elif parent.tag == "sub":
			pass
class div:
	element = None
	CSS = {}
	pad = 0
	cx = 0
	cy = 0
	texts = []
	def __init__(self, c, s, x, y, parent, w, h, t):
		cx = 0
		cy = 0
		try:
			self.element = c.create_rectangle(x,y,0,0, outline="")
			self.CSS = cssRead(s)
			if self.CSS != "ð":
				for elemit in parent:
					if elemit.tag in textag:
						self.texts.append(text(elemit,x,y,c,w,h,t, t))
					elif elemit.tag == "br":
						self.texts.append("←")
				if self.CSS != " ":
					c.itemconfigure(self.element, fill=self.CSS["background-color"])
				else:
					c.itemconfigure(self.element, fill="white")
				self.pad = sizeFormat(self.CSS["padding"], w)
				TLT = []
				for elem in self.texts:
					if elem != "←":
						c.coords(elem.element,self.cx, self.cy)
						self.cx += (w / (91 - elem.fonZise)) * len(elem.text)
						TLT.append(self.cx)
					else:
						self.cy += (h / 19)
						try:
							te = self.texts[self.texts.index(elem) + 1].element
							self.cx = 0
						except:
							pass
				self.cx = max(TLT)
				c.coords(self.element, x, y, self.cx + self.pad, self.cy + self.pad + (h / (10 + self.texts[0].fonZise)))
		except:
			pass
def cssRead (style):
	if style != "ł" or style!="" or style!=None:
		css = {"color":" ","background-color":" ","padding":" ","font-size":" "}
		if style != None:
			tcss = style.split(";")
			for cs in tcss:
				css[cs.split(":")[0]] = cs.split(":")[1].replace(" ","")
	else:
		css = "ð"
	if css != "ð":
		for sub in list(css):
			if css[sub] == " ":
				del css[sub]
	return css
def formaHTML (canvas, isL, h, w):
	canvas.delete("all")
	global xp, yp
	xp = 0
	yp = 0
	canvas.grid(row=0,column=1,sticky="we")
	isL  += " "
	f = os.popen("cd "+isL[0:isL.rfind("/")+1]+"; cat "+isL[isL.rfind("/")+1:-1]).read()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(f), parser).getroot()
	def format (body, xp, yp):
		for element in body:
			if element.tag == "div" or element.tag == "center":
				if "style" in element.attrib:
					if element.tag == "div":
						if "style" in element.attrib:
							ele = div(canvas, element.get("style"), xp, yp, element, w, h, NW)
						else:
							ele = div(canvas, "", xp, yp, element, w, h, NW)
					else:
						if "style" in element.attrib:
							ele = div(canvas, element.get("style"), w / 2, yp, element, w, h, NW)
						else:
							ele = div(canvas, "", w / 2, yp, element, w, h, N)
					yp += h / 19
					xp = 0
				else:
					if element.tag == "div":
						ele = div(canvas, "ł", xp, yp, element, w, h, NW)
					else:
						ele = div(canvas, element.get("style"), xp, yp, element, w, h, N)
			elif element.tag == "br":
				yp += h / 19
				xp = 0
			elif element.tag in textag:
				ele = text(element, xp, yp, canvas, w, h, 0, NW)
				xp += (ele.fonZise  - (ele.fonZise  / 2.5)) * len(ele.text)
				if "style" in element.attrib:
					tscss = cssRead(element.get("style"))
					if "padding" in element.get("style"):
						yp += (sizeFormat(tscss["padding"], w) * 2)
				bigText = ["h1","h2","h3","h4","h5","h6"]
				if element.tag in bigText:
					yp += h / (19 - int(element.tag[1]))
					xp = 0
				#TODO fix'd
	if "style" in tree[1].attrib:
		canvas.configure(bg = cssRead(tree[1].get("style").replace(" ",""))["background-color"].replace(" ",""))
	canvas.delete("all")
	format(tree[1], xp, yp)
def cssWrite(style):
	c = ""
	if not style == "":
		for sub in list(style):
			if style[sub] == " ":
				del style[sub]
		c = str(style).replace("{","").replace("}","").replace(",",";").replace('\'',"").replace("\"","")
	return c