#!/usr/bin/python
from tkinter import *
from tkinter import font as TF
import os
from lxml import etree
from io import StringIO, BytesIO
def formaHTML (canvas, isL, h, w):
	def find_all(a_str, sub):
		start = 0
		while True:
			start = a_str.find(sub, start)
			if start == -1: return
			yield start
			start += len(sub)
	canvas.grid(row=0,column=1,sticky="we")
	isL  += " "
	f = os.popen("cd "+isL[0:isL.rfind("/")+1]+"; cat "+isL[isL.rfind("/")+1:-1]).read()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(f), parser).getroot()
	body = tree[1]
	head = tree[0]
	jumpline = 0
	textTag = ["b","span","a","p","strong","i","em","mark","small","del","ins","sub","sup"]
	xp = 0
	for el in body:
		if el.tag in textTag:
			try:
				estilo = el.attrib["style"]
				if not estilo == '':
					css = cssForma(estilo)
					hp = h / 29 * jumpline
					fs = int(w / 75)
					if "px" in css["margin"]:
						xp += int(css["margin"][0:-2])
					if "px" in css["font-size"]:
						fs = css["font-size"][0:-2]
						fs = int(fs)
					elif "%" in css["font-size"]:
						ffs = int(css["font-size"][0:-1])
						fs = int((ffs / 75) * w / 100)
					else:
						fs = int(w / 75)
					if css["background-color"] != " ":
						fds = 0
						if "px" in css["padding"]:
							fds = int(css["padding"][0:-2])
						pos = [xp, hp + 1, xp * (len(el.text) + fds + 1), hp + fs * ((fds / fs + 1) + 0.5) + fds]
						canvas.create_rectangle(pos[0], pos[1], pos[2], pos[3], fill=css["background-color"], outline="")
					up = 0
					if el.tag == "b" or el.tag == "strong":
						isB = "bold"
					elif el.tag == "i":
						isB = "italic"
					elif el.tag == "sub":
						tf = ("Hervetica",int(w / 85))
						up = -2
					elif el.tag == "sup":
						tf = ("Hervetica",int(w / 85))
						up = 2
					else:
						isB = ""
					canvas.create_text(xp + fds,hp + fds + up,fill=css["color"],text=el.text, anchor=NW,font=(css["font-family"],fs, isB))
			except Exception as err:
			#	print(err)
				if el.tag == "b" or el.tag == "strong":
					tf = ("Helvetica",int(w / 75),"bold")
				else:
					tf = ("Helvetica",int(w / 75))
				col = "black"
				up = 0
				if el.tag == "a":
					col = "blue"
					tf = ("Helvetica",int(w / 75))
				elif el.tag == "i" or el.tag == "em":
					tf = ("Helvetica",int(w / 75), "italic")
				elif el.tag == "sub":
					tf = ("Hervetica",int(w / 85))
					up = -2
				elif el.tag == "sup":
					tf = ("Hervetica",int(w / 85))
					up = 2
				canvas.create_text(xp + 1,h / 29 * jumpline + up,fill=col,text=el.text, anchor=NW,font=tf)
			if el.tag == "br":
				xp = 0
			else:
				fs = int(w / 105) * len(el.text)
				xp += fs
		if el.tag == "br":
			jumpline += 1
			xp = 0
def cssForma (str):
	cascade = str.split(";")
	css ={
"color":"black",
"font-family":"Helvetica",
"font-size":" ",
"background-color":" ",
"padding":"1px",
"margin": "5px"
}
	for e in cascade:
		css[e.split(":")[0]] = e.split(":")[1]
	return css
