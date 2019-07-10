from tkinter import *
from tkinter import ttk
from lxml import etree
from io import StringIO, BytesIO
from src.lib.formaHtml import cssRead
import os
xp = 0
yp = 0
textTag = ["b","i","sup","sub","span","h1","h2","h3","h4","h5","h6"]
class text:
	def __init__(self,elem,par):
		element = etree.fromstring(elem)
		t = Label(par,text=element.text)
		t.grid(row=yp,column=xp,sticky=N+W)
		if "style" in element.attrib:
			css = cssRead(element.get("style"))
			if "background-color" in css.keys():
				t["bg"] = css["background-color"]
			else:
				t["bg"] = t.master["bg"]
			if "color" in css.keys():
				t.configure(fg=css["color"])
		else:
			t["bg"] = t.master["bg"]
			t.configure(fg="black")
def formaHTML (canvas, isL):
	for element in canvas.winfo_children():
		element.destroy()
	inf =  os.popen("cat "+ isL).read()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(inf), parser).getroot()
	if "style" in tree[1].attrib:
		css = cssRead(tree[1].get("style"))
		if "background-color" in css.keys():
			canvas.configure(bg=css["background-color"])
	for elemint in tree[1]:
		parOne(canvas,etree.tostring(elemint))
def parOne (parent,data):
	if len(data) > 1:
		ele = etree.fromstring(data)
		global xp, yp
		if ele.tag in textTag:
			text(etree.tostring(ele), parent)
			xp += 1
			if ele.tag in ["h1","h2","h3","h4","h5","h6"]:
				xp = 0
				yp += 1
		elif ele.tag == "br":
			xp = 0
			yp += 1