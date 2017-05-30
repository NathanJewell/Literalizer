import math
import numpy as np


namefile = open('names.txt', "r");
textfile = open('book.txt', "r");

names = [];

#array of size name by name to hold all data eg...
#spots hold calculated relationship between two names
#
#
#
#
#

for name in namefile:
	names.append(name.strip("\n"));

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

def scrapeText(w, t):   #word can be colon seperated list of words
    indices = []
    for it in range(len(t)):
        if check(w, t[it]):
            indices.append(it)
    return indices
#character importance over time

#i think N^2 complexity rn so probs < 10 names ideally

#rank absolute importance of characters
    #total number of name instances
    #seperation of name instances
#map the importance of characters relative to one another
    #proximity of name instances

#scraping for all indices of all names
indices = []
for n1 in names:
    indices.append(scrapeText(n1, text))


counts = [len(indices[a])*1000 for a in range(len(indices))]  #total count of that name in text --- larger is better
#seperation can just be average distance between -- smaller is better
#non-linear because otherwise it would just equal the total length of text
#punishing larger distances and rewarding smaller distances
seperations = []
for i in range(len(indices)):
    last = 0;
    seperation = 0;
    for index in indices[i]:
        seperation += pow((index-last),2)
        last = index
    seperation/=counts[i]
    seperations.append(seperation)

absolutes = dict(zip(names,[counts[a]/seperations[a] for a in range(len(seperations))]))


#total score by division
# seperation was allready divided by counts but that was not really applying the filter just accounting for natural reason

#relative importance of characters
#proximity search size
size = 1500  #how many words to look from center
relations = [] #scalar summative difference higher is better
for n1 in range(len(indices)):
    df = []
    for n2 in range(n1+1, len(indices)):    #adding +1 here is optimization because the first will always be the same as the one it is checking against
        diff = 0
        if n1 != n2:
            for it in range(len(indices[n1])):
                index = indices[n1][it]
                for itt in range(len(indices[n2])):
                    d = abs(index - indices[n2][itt])
                    if d < size:
                        diff += 1/d
        df.append(diff)
    relations.append(dict(zip(names[n1+1:], df)))

relations = dict(zip(names,relations))
                    #need to optimize for skipping the extras really badly

#writing to file now
web = open('web.txt', "w");

for n, v in absolutes.items():
    web.write(n + "," + str(v)+"\n")

web.write("RELATIONING\n")    #tells visualizer to switch reading modes

for n1, dic in relations.items():
    for n2, v in dic.items():
        web.write(n1+","+n2+","+str(v)+"\n")

web.close()
