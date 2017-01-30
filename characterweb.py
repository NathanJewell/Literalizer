import math
import plotly.plotly as py
import plotly as ploty
ploty.tools.set_credentials_file(username='ncjewell', api_key='jI34UQmdCtM4pY3cOxBA')
import plotly.graph_objs as go
import numpy as np


namefile = open('names.txt', "r");
textfile = open('book.txt', "r");
webf = open('web.txt', "w");

names = [];

#array of size name by name to hold all data eg...
#spots hold calculated relationship between two names
#
#
#
#
#

web = dict() 	#name1,name2 : seperations
ind = dict()

for name in namefile:
	names.append(name.strip("\n"));

print(names)
text = [word for line in textfile for word in line.split()]


last = 0
this = 0
current = ""

def switch(c, a, b):
	if(c == a):
		return b
	return a

def check(arr, word):
	for name in arr.split(":"):
		if name == word:
			return True
	return False

for n in names:
	name = n.split(",")
	seperations = []
	indices = []
	#finding first instance of either word
	for it in range(len(text)):
		if check(name[0],text[it]):
			current = name[1]
			break
		elif check(name[1],text[it]):
			current = name[0]
			break
		this = it;
	#iterating through all words
	for it in range(len(text)):	
		if check(current,text[it]):
			current = switch(current, name[0], name[1]);
			last = this
			this = it
			seperations.append(this-last);	#adding difference between indices
			indices.append(it)

	web[name[0][0]+","+name[1][0]] = seperations
	ind[name[0][0]+","+name[1][0]] = indices

print(web)
print(len(text))

traces = [];

for key in web:
	traces.append(go.Histogram(
		x = ind[key],
		y = web[key],
		#mode = 'lines',
		opacity = .7,
		name = key
	))

layout = go.Layout( 
	barmode = 'overlay'
)

fig = go.Figure(data=traces, layout=layout);

py.plot(fig, filename='ifobPLOT')

def connectionstrength(seperations):
	print("nothing")
	#sort
	#remove outliers
	#find mean, Sx