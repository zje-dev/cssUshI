#!/usr/bin/python
from tkinter import *
from tkinter import font as TF
import os
from lxml import etree
from io import StringIO, BytesIO
def formaHTML (canvas, isL, h, w):
	canvas.grid(row=0,column=1,sticky="we")
	isL  += " "
	f = os.popen("cd "+isL[0:isL.rfind("/")+1]+"; cat "+isL[isL.rfind("/")+1:-1]).read()
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO(f), parser).getroot()
