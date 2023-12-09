import torch
from datetime import datetime
from transformers import pipeline
import tkinter.messagebox
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import *
from tkinter import font
from utils import *

print('Starting. Setting up system. This will take a while ...')
setup_logging()
logging.info(f"\n{'='*50}\nNew Session: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n{'='*50}")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
logthis(f"LLM will be running on {device}")

logthis(f"Loading pipeline")
generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B', device=device)
# generator = pipeline('text-generation', model='PygmalionAI/pygmalion-2-7b', device=device)
logthis(f"Loading pipeline DONE")


@monitor_fn
def clear_prompt():
    output_field.delete(1.0,"end")

@monitor_fn
def process_text():
    global generator
   
    ##### Vanilla Huggingface Transformer Text Generation #####
    logthis('   Button Pressed')
    prompt = prompt_field.get()
    logthis(f"   prompt:\n{prompt}")
    logthis('   calling LLM')
    result = generator(prompt, min_length=200, max_length=210, do_sample=True, temperature=0.89)
    logthis('   LLM call done')
    raw_result = (result[0]['generated_text'])
    logthis(f'   result"\n{raw_result}')
    
    ##### Generate indexes for sentence ending punctuation #####
    logthis('   postprocessing result')
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

    answer = trimmer(period,question_mark,exclamation_mark,quotes)
    logthis('   postprocessing done')
    logthis(f'   result"\n{answer}')
    
    output_field.insert(1.0,answer)
    logthis('   -------------------------------------')


win=tkinter.Tk()
win.title("A.N.N.A.")
win.geometry('1920x950+20+20')
win['background']= '#000147'

zmack_label=Label(win, text="ZMACK! Presents: A.N.N.A.", font=('rog fonts', 30, 'bold'),height=2,background='#000147', foreground='#4fe3d7')
zmack_label.grid(row=0,columnspan=3,column=0, sticky='w')

prompt_label=Label(win, text="What is on your mind?", font=('rog fonts', 16, 'bold'),background='#000147',foreground='#4fe3d7')
prompt_label.grid(row=1,column=0, sticky='w')

prompt_field=Entry(win,bd=5,font=('terminal', 16),background='#c6f6f2')
prompt_field.grid(row=1,column=1,ipadx=200,sticky='w')

prompt_enter=Button(win,text='Submit',font=('rog fonts', 32),command=process_text,background='#000147',foreground='#4fe3d7',activebackground='#4fe3d7',activeforeground='#000147')
prompt_enter.grid(row=1,column=2,sticky='w')

loading_label=Label(win, text="", font=('terminal',20, 'bold'),background='#000147',foreground='#4fe3d7')
loading_label.grid(row=2,columnspan=2,column=1)

output_label=Label(win, text="Response", font=('rog fonts', 16, 'bold'),background='#000147',foreground='#4fe3d7')
output_label.grid(row=3,column=0, sticky='w')

output_field=Text(win,bd=5, height=17, width=49, wrap='word',font=('terminal', 24),background='#c6f6f2')
output_field.grid(row=3,columnspan=2,column=1, sticky='w')

prompt_clear=Button(win,text='Clear',font=('rog fonts', 16, 'bold'), command=clear_prompt,background='#000147',foreground='#4fe3d7',activebackground='#4fe3d7',activeforeground='#000147')
prompt_clear.grid(row=4,columnspan=2,column=1)

win.mainloop()