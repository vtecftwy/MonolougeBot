from turtle import color
from transformers import pipeline
import tkinter.messagebox
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import *
from tkinter import font


generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')
#=====================================================
def clear_prompt():
    output_field.delete(1.0,"end")

def process_text():
    global generator
   
    ##### Vanilla Huggingface Transformer Text Generation #####
    print('Button Pressed')
    prompt = prompt_field.get()
    print(prompt)
    '''prompt = input("What is on your mind?: ")'''
    
    result = generator(prompt,min_length=300, max_length=400 , do_sample=True, temperature=0.89)
    raw_result = (result[0]['generated_text'])
    
    ##### Generate indexes for sentence ending punctuation #####
    period = raw_result.rfind(".") 
    question_mark = raw_result.rfind("?")
    exclamation_mark =  raw_result.rfind("!")
    quotes = raw_result.rfind('"')         

    # Function compares the 4 index values, slices the end off of the largest,returns the raw result minus the hanging sentence fragment #####
    def trimmer(a, b, c, d):
        if a > b and a > c and a > d:                                   
            return raw_result[:a+1]
        elif b > a and b > c and b > d:
            return raw_result[:b+1]
        elif c > a and c > b and c >d:
            return raw_result[:c+1]
        else:
            return raw_result[:d+1]

    '''print(trimmer(period,question_mark,exclamation_mark,quotes))'''

    answer = trimmer(period,question_mark,exclamation_mark,quotes)
    
    
    output_field.insert(1.0,answer)
    
#=====================================================


win=tkinter.Tk()
win.title("A.N.N.A.")
win.geometry('1250x950+20+20')

zmack_label=Label(win, text="ZMACK! Presents: A.N.N.A.", font=('rog fonts', 30, 'bold'), height=2)
zmack_label.grid(row=0,columnspan=3,column=0, sticky='w')

prompt_label=Label(win, text="What is on your mind?", font=('rog fonts', 16, 'bold'))
prompt_label.grid(row=1,column=0, sticky='w')

prompt_field=Entry(win,bd=5,font=('terminal', 16))
prompt_field.grid(row=1,column=1,ipadx=200,sticky='w')

prompt_enter=Button(win,text='Submit',font=('rog fonts', 32),command=process_text)
prompt_enter.grid(row=1,column=2,sticky='w')

loading_label=Label(win, text="", font=('terminal',20, 'bold'))
loading_label.grid(row=2,columnspan=2,column=1)

output_label=Label(win, text="Response", font=('rog fonts', 16, 'bold'))
output_label.grid(row=3,column=0, sticky='w')

output_field=Text(win,bd=5, height=17, width=49, wrap='word',font=('terminal', 24))
output_field.grid(row=3,columnspan=2,column=1, sticky='w')

prompt_clear=Button(win,text='Clear',font=('rog fonts', 16, 'bold'), command=clear_prompt)
prompt_clear.grid(row=4,columnspan=2,column=1)



win.mainloop()