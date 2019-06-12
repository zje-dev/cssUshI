#!/usr/bin/python
from tkinter import *
import os
from lxml import etree
from io import StringIO, BytesIO
px = 0
py = 0
textag = ["span","b","i","sub","sup","h1","h2","h3","h4","h5","h6"]
class text:
	CSS = {}
	fonZise = 0
	def __init__(self, parent, x, y, c):
		if parent.tag == "span":
			if "style" in parent.attrib:
				self.CSS = cssRead(parent.get("style"))
			if "font-size" in parent.get("style"):
				pass
			else:
				if parent.tag == "h6":
					self.fonZise = 5
				elif parent.tag == "h5":
					self.fonZise = 8
				elif parent.tag == "h4":
					self.fonZise = 12
				elif parent.tag == "h3":
					self.fonZise = 16
				elif parent.tag == "h2":
					self.fonZise = 36
				elif parent.tag == "h1":
					self.fonZise = 40
				else:
					self.fonZise = 16
		c.create_text(x, y, text=parent.text, anchor=NW, fill="black", font=("Arial", self.fonZise))
class div:
	element = None
	CSS = {}
	pad = 0
	cx = 0
	cy = 0
	def __init__(self, c, s, x, y, parent, w, h):
		self.element = c.create_rectangle(x,y,0,0, outline="")
		self.CSS = cssRead(s)
		if self.CSS != "ð":
			for elemit in parent:
				if elemit.text != None:
					self.cx += len(elemit.text) * w / 79
					tex = text(elemit,x,y,c)
			c.itemconfigure(self.element, fill=self.CSS["background-color"])
			if "px" in self.CSS["padding"]:
				self.pad = float(self.CSS["padding"].replace("px", ""))
			elif "%" in self.CSS["padding"]:
				self.pad = w / (100 / float(self.CSS["padding"][0:-1]))
			else:
				self.pad = float(self.CSS["padding"].replace("px",""))
			c.coords(self.element, x, y, self.cx + self.pad, self.cy + self.pad)
			global px, py
			px += self.pad
			py += self.pad
	def editar ():
		pass
def cssRead (style):
	if style != "ł":
		css = {"color":"black","background-color":"white","padding":"1px","font-size":"14px"}
		tcss = style.split(";")
		for cs in tcss:
			css[cs.split(":")[0]] = cs.split(":")[1]
	else:
		css = "ð"
	return css
def formaHTML (canvas, isL, h, w):
	global xp, yp
	canvas.grid(row=0,column=1,sticky="we")
	isL  += " "
	f = os.popen("cd "+isL[0:isL.rfind("/")+1]+"; cat "+isL[isL.rfind("/")+1:-1]).read()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(f), parser).getroot()
	def format (body, xp, yp):
		for element in body:
			if element.tag == "div":
				if "style" in element.attrib:
					ele = div(canvas, element.get("style"), xp, yp, element, w, h)
				else:
					ele = div(canvas, "ł", xp, yp, element)
			elif element.tag == "br":
				yp += h / 20
			elif element.tag in textag:
				ele = text(element, xp, yp, canvas)
	if "style" in tree[1].attrib:
		canvas.configure(bg = cssRead(tree[1].get("style"))["background-color"])
	canvas.delete("all")
	format(tree[1], px, py)
