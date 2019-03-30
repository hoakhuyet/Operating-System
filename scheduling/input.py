#!/usr/bin/python3

from Tkinter import *

import os
fields = 'Process ID', 'Arrival Time', 'Duration', 'Priority'
file = 'atom Desktop/SourceCpuScheduling/data.txt'
filelog = 'atom Desktop/SourceCpuScheduling/log.txt'

def printToFile(entries):
    contents = ''
    for entry in entries:
        text  = entry[1].get()
        contents += text + ' '
    contents += '\n'
    file = open('data.txt', 'a')
    file.write(contents)
    file.close()

def makeform(root, fields):
    entries = []
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=15, text=field, anchor='w')
        ent = Entry(row)
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=NO, fill=X)
        entries.append((field, ent))

    return entries

def openFile(x):
    if x == 1:
        os.system(file)
    elif x == 2:
        os.system('python FIrstComeFirstServed.py')
    else:
        os.system(filelog)

if __name__ == '__main__':
   root = Tk()
   root.title("CPU SCHEDULING")
   root.geometry('250x200')

   ents = makeform(root, fields)
   root.bind('<Return>', (lambda event, e=ents: printToFile(e)))
   b1 = Button(root, text='Add Process',
          command=(lambda e=ents: printToFile(e)))
   b1.pack(side=LEFT, padx=5, pady=5)

   root.mainloop()
