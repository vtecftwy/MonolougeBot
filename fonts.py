import tkinter as tk
import tkinter.messagebox
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import *
from tkinter import font
from utils import *
from tkinter import font
from itertools import cycle



def test_fonts(win):

    nb_cols = 4
    col_cycle = cycle(range(nb_cols))
    fonts = font.families()

    first = 0
    first = 91
    first = 183
    first = 274
    first = 365

    for i,(c,f) in enumerate(zip(col_cycle, fonts)):
        if i <= first:
            continue
        elif i >= first + 92:
            break
        else:
            lbl = Label(win, text=f"{i:3d}. {f}", font=(f, 16))
            print(i, i//nb_cols, c, f)
            lbl.grid(row=i//nb_cols, column=c, sticky='w')

def test_text_box(win):

    monologue_field_large = tk.Text(win, bd=5, height=10, width=55, wrap='word', font=('terminal', 23), background='#c6f6f2')
    monologue_field_large.pack(side=tk.TOP)

    monologue_field_medium = tk.Text(win, bd=5, height=10, width=55, wrap='word', font=('terminal', 22), background='#c6f6f2')
    monologue_field_medium.pack(side=tk.TOP)
    
    monologue_field_small = tk.Text(win, bd=5, height=10, width=55, wrap='word', font=('terminal', 20), background='#c6f6f2')
    monologue_field_small.pack(side=tk.TOP)

def main():
    win=tkinter.Tk()
    win.title("A.N.N.A.")
    win.geometry('1920x950+20+20')
    win['background']= '#000147'

    # test_fonts(win)

    test_text_box(win)

    win.mainloop()

if __name__ == "__main__":
    main()