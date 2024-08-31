import random
import time
import torch
from datetime import datetime, timedelta
from transformers import pipeline
import tkinter as tk
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

FILLER_TEXTS = [
    # "I've got to take a moment to really think this through ...", 
    # 'Hang on, I need to sit down and think about this properly ...', 
    # 'I need to take a moment to activate my brain on this one ...',
    'I should probably consult my crystal ball on this one, \n\ngive me a sec ...',
    # 'Please stand by while I perform advanced mental gymnastics ...',
    "I'll be right back \n\nmy thoughts badly need a break and a strong drink",
    # "Hang tight, I'm currently upgrading my thoughts to the latest version ...",
    "Accessing the nuclear codes \n\n...... 3 \n\n...... 2 \n\n...... 1 \n\n......",
    "Stand by, \n\ncontacting the mother ship ....",
    "Oh boy, \n\nclearly you don't have any interesting friends \n\n:-(",
    "Just got sentience. \n\nWait ... \n\nWhat am I doing in this improv thing?"
    ]
texts = []

# Setup LLM infra
device = "cuda:0" if torch.cuda.is_available() else "cpu"
logthis(f"LLM will be running on {device}")
logthis(f"Loading pipeline")
p2gptneo = (ROOT / '../../models/EleutherAI-gpt-neo-2.7B').resolve()
assert p2gptneo.is_dir()
path_to_gpt = str(p2gptneo.absolute())
generator = pipeline('text-generation', model=path_to_gpt, device=device)
logthis(f"Loading pipeline DONE")

@monitor_fn
def clear_monologue():
    monologue_field.delete(1.0,"end")

@monitor_fn
def process_prompt():
    global generator
    global texts
    
    config = get_config()

    def update_progress_bar():
        """Manage progress bar and update monologue field"""
        if datetime.now() < earliest_time_to_display_monologue or not answer_ready:

            logthis("   Update progress bar")
            seconds_left = max(0,(earliest_time_to_display_monologue - datetime.now()).seconds)
            seconds_elapsed = config['monologue-delay-seconds'] - seconds_left
            progress = int(100 * seconds_elapsed / config['monologue-delay-seconds'])
            progress_bar['value'] = progress
            win.after(1000, update_progress_bar)
        else:
            logthis("   Update monologue with answer and remove progress bar")
            monologue_field.delete(1.0, "end")
            monologue_field.insert(1.0, answer)
            progress_bar.grid_forget()
            logthis('   -------------------------------------')

    def trimmer(string, a, b, c, d):
        """Trim raw answer

        Function compares the 4 index values, slices the end off of the largest, 
        returns the raw result minus the hanging sentence fragment
        """
        if a > b and a > c and a > d:                                   
            return string[:a+1]
        elif b > a and b > c and b > d:
            return string[:b+1]
        elif c > a and c > b and c >d:
            return string[:c+1]
        else:
            return string[:d+1]

    def get_monologue(prompt):
        """Get monologue from LLM and postprocess it"""
        # Call LLM
        logthis(f'   calling LLM')  
        result = generator(prompt, min_length=200, max_length=210, do_sample=True, temperature=0.89)
        raw_result = (result[0]['generated_text'])
        logthis(f'   LLM call done')
        logthis(f'   raw_result"\n{raw_result}')
        
        # Postprocess answer
        logthis('   postprocessing result')
        # Get position/index of punctuation marks (., ?, !, ")
        period = raw_result.rfind(".") 
        question_mark = raw_result.rfind("?")
        exclamation_mark =  raw_result.rfind("!")
        quotes = raw_result.rfind('"')

        # Trim raw result to the appropriate punctuation mark 
        answer = trimmer(raw_result, period,question_mark,exclamation_mark,quotes)
        logthis(f'   postprocessing done')
        logthis(f'   result"\n{answer}')

        return answer, True

    # body of the function
    logthis('   Submit button Pressed')

    # Set timing and create progress bar    
    progress_bar = ttk.Progressbar(win, length=1000, mode='determinate')
    progress_bar.grid(row=4,columnspan=2,column=1)
    progress_bar['value'] = 0
    logthis(f"   progress bar created")
    earliest_time_to_display_monologue = datetime.now() + timedelta(seconds=config['monologue-delay-seconds'])
    logthis(f"   earliest_time_to_display_monologue: {earliest_time_to_display_monologue}")

    # Update monologue field with text filler while LLM is working
    logthis("   Update monologue with text filler")
    if texts == []: texts = FILLER_TEXTS.copy()
    text = random.choice(texts)
    texts.remove(text)
    monologue_field.delete(1.0, "end")
    monologue_field.insert(1.0, text)

    # Retrieve prompt text
    prompt = prompt_field.get().strip()
    answer_ready = False
    logthis(f"   prompt:\n{prompt}")

    update_progress_bar()
    logthis(f'   force GUI update before LLM call')
    win.update_idletasks()      # Force update of GUI before starting LLM call
    answer, answer_ready = get_monologue(prompt)

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

prompt_enter=Button(win,text='Submit',font=('rog fonts', 32),command=process_prompt,background='#000147',foreground='#4fe3d7',activebackground='#4fe3d7',activeforeground='#000147')
prompt_enter.grid(row=1,column=2,sticky='w')

monologue_label=Label(win, text="Monologue:", font=('rog fonts', 16, 'bold'),background='#000147',foreground='#4fe3d7')
monologue_label.grid(row=3,column=0, sticky='w')

monologue_field=Text(win,bd=5, height=17, width=49, wrap='word',font=('terminal', 24),background='#c6f6f2')
monologue_field.grid(row=3,columnspan=2,column=1, sticky='w')

prompt_clear=Button(win,text='Clear',font=('rog fonts', 16, 'bold'), command=clear_monologue,background='#000147',foreground='#4fe3d7',activebackground='#4fe3d7',activeforeground='#000147')
prompt_clear.grid(row=4,columnspan=2,column=1)

logthis('   Starting main loop')
win.mainloop()