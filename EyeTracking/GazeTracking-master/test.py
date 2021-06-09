import tkinter
from tkinter import *

window = tkinter.Tk()
window.title("Eye Tracking")
window.minsize("300", "100")

label = Label(window, text="Nome: ")
label.pack()

labelInput = StringVar()
labelInput = Entry(window, textvariable=labelInput)
labelInput.pack()

button = Button(window, text="Next")
button.pack()

window.mainloop()