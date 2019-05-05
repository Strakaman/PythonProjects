#python 2.7
from Tkinter import *
import Tkinter as tk
import time 
import csv 
from PIL import Image, ImageTk

class Element:
	name = ""
	icon = ""
	mixResults=[]
	photo =""

	def __init__(self):
		return
	
def initVals():
	elementsList = []
	with open("elements.csv", 'r') as f:
		next(f)  # skips headings
		reader = csv.reader(f, delimiter=',')
		for eName, lMix, eMix, wiMix, waMix,fMix, ico in reader:
			e = Element()
			e.name = eName
			e.mixResults = [lMix, eMix, wiMix, waMix, fMix]
			print(e.mixResults)
			e.icon = ico
			image = Image.open(ico).resize((225, 225), Image.ANTIALIAS)
			e.photo = ImageTk.PhotoImage(image)
			elementsList.append(e)
	return elementsList

def showElement(evt):
	w = evt.widget
	index = int(w.curselection()[0])
	elementPic.configure(image = eList[index].photo)
	print 'You selected item %d: "%s"' % (index, eList[index].icon)
	global cachedIndex
	if cachedIndex == index:
		return
	cachedIndex = index
	comboImgIndex = 0
	for i in range(len(eList)):
		#print ("I:" + str(i)+ " index:" +str(index) + " comboindex:" + str(comboImgIndex))
		if i == (4-index):
			#since we are not displaying combo when elements are combined with itself, skip whenever loop
			#iterator and combo element would be the same element
			continue
		else:
			resizedImage2 = Image.open("Combos\\"+eList[index].mixResults[i]+".png").resize((225, 225), Image.ANTIALIAS)
			comboPhoto2 = ImageTk.PhotoImage(resizedImage2)
			comboImageLabels[comboImgIndex].configure(image = comboPhoto2)
			comboImageLabels[comboImgIndex].img = comboPhoto2
			comboImgIndex += 1
		'''comboPhoto = ImageTk.PhotoImage(resizedImage)
			comboImageLabel = tk.Label(bottomRightFrame, image=comboPhoto, borderwidth=3, relief="solid", width=225,
									   height=225)
			comboImageLabel.grid(row=r, column=c)
			comboImageLabel.img = comboPhoto
			comboImageLabels[r][c] = comboImageLabel'''


# Initialize Tkinter window
window = Tk()
window.geometry("725x700") # Create geometry of window to fit necessary widgets
window.resizable(0,0) # disable resizability
window.title("Element Matrix") 

eList = initVals()
cachedIndex = -1

leftSide = PanedWindow()
leftSide.pack(fill=BOTH, expand=1)

frame = LabelFrame(window, text="Left Window",bg = "Gray", height = 550,width = 280,bd=10)
#frame.pack( side = LEFT, expand="yes")
leftSide.add(frame)
rightSide = PanedWindow(leftSide, orient=VERTICAL)
leftSide.add(rightSide)

#top = Label(rightSide, text="top pane")
#rightSide.add(top)

dataFrame = LabelFrame(window, text="Data",bg = "White", height = 350,width = 280,bd=5)

elementLabel = Label(dataFrame, text = "ELEMENT MATRIX", font=("Helvetica", 32), bg= "White")
elementLabel.pack(side = TOP)
elementPic = tk.Label(frame, image=eList[0].photo)
elementPic.img = eList[1].photo
elementPic.pack(side = BOTTOM)

colorList = ["Red", "Blue", "White", "Brown", "Yellow"]
m3 = PanedWindow(dataFrame)
m3.pack(side=TOP)

gridLabels=[[0 for x in range(6)] for y in range(6)]
for i in range (6):
	for j in range (6):
		bgColor = "White"
		if i==0 or j==0:
			bgColor = "Black"
		gridLabel = Label(m3,text="",borderwidth=3,bg=bgColor, relief=GROOVE, width=8)
		gridLabel.grid(row=i,column=j)
		gridLabels[i][j] = gridLabel
	if i>0:
		#if not the header row, print all the elemental combos
		gridLabels[i][1]['text']=eList[i-1].mixResults[0]
		gridLabels[i][2]['text']=eList[i-1].mixResults[1]
		gridLabels[i][3]['text']=eList[i-1].mixResults[2]
		gridLabels[i][4]['text']=eList[i-1].mixResults[3]
		gridLabels[i][5]['text']=eList[i-1].mixResults[4]
for i in range (1,6):
	#top row
	gridLabels[0][6-i]['text'] = eList[i-1].name
	gridLabels[0][6-i]['fg'] = colorList[i-1]
	#left column
	gridLabels[i][0]['text'] = eList[i-1].name
	gridLabels[i][0]['fg'] = colorList[i-1]
	
dataFrame.pack( side = RIGHT)
rightSide.add(dataFrame)

bottomRightFrame = Frame(window, height = 350,width = 280,bd=5)
rightSide.add(bottomRightFrame)

comboImageLabels=[]
for r in range(2):
	for c in range(2):
		#resizedImage = Image.open("Combos\metal.png").resize((225,225),Image.ANTIALIAS)
		#comboPhoto = ImageTk.PhotoImage(resizedImage)
		comboImageLabel = tk.Label(bottomRightFrame, image="", borderwidth = 3, relief="solid",width=225,height=225)
		comboImageLabel.grid(row=r,column=c)
		#comboImageLabel.img = comboPhoto
		comboImageLabels.append(comboImageLabel)

Lb1 = Listbox(frame, height = 40,width = 25)
for index,element in enumerate(eList, start=0):
	Lb1.insert(index,element.name)

Lb1.bind('<<ListboxSelect>>', showElement)
Lb1.pack()

#bind $::Lb1 <<ListboxSelect>> "showElement"

window.mainloop()
