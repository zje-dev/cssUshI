#!/usr/bin/python
from tkinter import *
import os
from lxml import etree
from io import StringIO, BytesIO
xp = 0
yp = 0
textag = ["span","b","i","sub","sup","h1","h2","h3","h4","h5","h6"]
def sizeFormat (s, w):
	z = 0
	if "px" in s:
		z = float(s.replace("px", ""))
	elif "%" in s:
		z = w / (100 / float(s[0:-1]))
	else:
		z = float(s)
	return z
class text:
	CSS = {}
	fonZise = 0
	texType = "normal"
	text = ""
	color = "black"
	def __init__(self, parent, x, y, c, w, h, t):
		self.text = parent.text
		def fz (me, par):
			if par.tag == "h6":
				me.fonZise = 6
			elif par.tag == "h5":
				me.fonZise = 10
			elif par.tag == "h4":
				me.fonZise = 14
			elif par.tag == "h3":
				me.fonZise = 17
			elif par.tag == "h2":
				me.fonZise = 20
			elif par.tag == "h1":
				me.fonZise = 25
			else:
				me.fonZise = 16
		fz(self, parent)
		if "style" in parent.attrib:
			self.CSS = cssRead(parent.get("style"))
			if parent.tag == "span":
				if "font-size" in parent.get("style"):
					self.fonZise = sizeFormat(self.CSS["font-size"], w)
		if parent.tag == "b":
			self.texType = "bold"
		if len(self.CSS) > 0:
			self.color = self.CSS["color"]
		c.create_text(x, y, text=parent.text, anchor=NW, fill=self.color, font=("Arial", self.fonZise, self.texType))
class div:
	element = None
	CSS = {}
	pad = 0
	cx = 0
	cy = 0
	def __init__(self, c, s, x, y, parent, w, h, t):
		self.element = c.create_rectangle(x,y,0,0, outline="")
		self.CSS = cssRead(s)
		if self.CSS != "ð":
			for elemit in parent:
				if elemit.text != None:
					self.cx += len(elemit.text) * w / 79
					tex = text(elemit,x,y,c,w,h,t)
			c.itemconfigure(self.element, fill=self.CSS["background-color"])
			self.pad = sizeFormat(self.CSS["padding"], w)
			c.coords(self.element, x, y, self.cx + self.pad, self.cy + self.pad)
			global xp, yp
			xp += self.pad
			yp += self.pad
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
					ele = div(canvas, element.get("style"), xp, yp, element, w, h, 0)
				else:
					ele = div(canvas, "ł", xp, yp, element, 0)
			elif element.tag == "br":
				yp += h / 19
				xp = 0
			elif element.tag in textag:
				ele = text(element, xp, yp, canvas, w, h, 0)
				xp += ele.fonZise * len(ele.text)
				if "style" in element.attrib:
					tscss = cssRead(element.get("style"))
	if "style" in tree[1].attrib:
		canvas.configure(bg = cssRead(tree[1].get("style"))["background-color"])
	canvas.delete("all")
	format(tree[1], xp, yp)
