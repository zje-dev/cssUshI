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
		#if "style" in element.atrib:
		Label(par,text=element.text).grid(row=yp,column=xp,sticky=N+W)
def formaHTML (canvas, isL):
	inf =  os.popen("cat "+ isL).read()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(inf), parser).getroot()
	for elemint in tree[1]:
		parOne(canvas,etree.tostring(elemint))
def parOne (parent,data):
	ele = etree.fromstring(data)
	global xp, yp
	if ele.tag in textTag:
		text(etree.tostring(ele), parent)
		xp += 1
	elif ele.tag == "br":
		xp = 0
		yp += 1