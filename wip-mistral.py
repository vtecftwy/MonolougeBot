import torch
from datetime import datetime
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
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
p2mistral = (ROOT / '../../models/Mistral-7B-Instruct-v0.2-GPTQ').resolve()
assert p2mistral.is_dir()
path_to_mistral = str(p2mistral.absolute())
model = AutoModelForCausalLM.from_pretrained(path_to_mistral,
                                             device_map="auto",
                                             trust_remote_code=False,
                                             revision="main")
tokenizer = AutoTokenizer.from_pretrained(path_to_mistral, use_fast=True)
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
    top_p=0.95,
    top_k=40,
    repetition_penalty=1.1
)
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
    system_prompt = '''You are in an Improv team playing an Armando game. Your role is to tell the monologue that will inspire the scenes. 
    Tell us your monologue based on the following prompt. Only give us what you will say, not your attitudes or comments about the scene and audience'''
    prompt_model=f'''<s>[INST] {system_prompt}: {prompt} [/INST]'''
    
    
    result = generator(prompt_model, min_length=200, max_length=210, do_sample=True, temperature=0.89)
    logthis('   LLM call done')
    raw_result = (result[0]['generated_text'])
    logthis(f'   result"\n{raw_result}')
    filtered_result = raw_result.replace(f"<s>[INST] {system_prompt}: ", '').replace(' [/INST]', '')
    logthis(f'   filtered result"\n{filtered_result}')
    
    ##### Generate indexes for sentence ending punctuation #####
    logthis('   postprocessing result')
    period = filtered_result.rfind(".") 
    question_mark = filtered_result.rfind("?")
    exclamation_mark =  filtered_result.rfind("!")
    quotes = filtered_result.rfind('"')
    

    # Function compares the 4 index values, slices the end off of the largest,returns the raw result minus the hanging sentence fragment #####
    def trimmer(a, b, c, d):
        if a > b and a > c and a > d:                                   
            return filtered_result[:a+1]
        elif b > a and b > c and b > d:
            return filtered_result[:b+1]
        elif c > a and c > b and c >d:
            return filtered_result[:c+1]
        else:
            return filtered_result[:d+1]

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