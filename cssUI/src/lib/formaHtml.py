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
	textTag = ["b","span"]
	xp = 0
	for el in body:
		if el.tag in textTag:
			try:
				estilo = el.attrib["style"]
				if not estilo == '':
					css = cssForma(estilo)
					canvas.create_text(xp,h / 29 * jumpline,fill=css["color"],text=el.text, anchor=NW,font=(css["font-family"],int(w / 75), 'bold'))
			except Exception as err:
				#print(err)
				if el.tag == "b":
					tf = ("Helvetica",int(w / 75),"bold")
				else:
					tf = ("Helvetica",int(w / 75))
				canvas.create_text(xp,h / 29 * jumpline,fill="black",text=el.text, anchor=NW,font=tf)
			try:
				prev = body[body.index(el) + 1]
				if prev.tag == "br":
					xp = 0
				else:
					xp += w / 75 * len(el.text)
			except:
				xp=0
		if el.tag == "br":
			jumpline += 1
			xp = 0
def cssForma (str):
	cascade = str.split(";")
	css ={
"color":"black",
"font-family":"Helvetica"
}
	for e in cascade:
		css[e.split(":")[0]] = e.split(":")[1]
	return css

