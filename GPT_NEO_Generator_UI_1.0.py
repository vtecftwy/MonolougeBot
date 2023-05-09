from turtle import color
from transformers import pipeline
from diffusers import __version__
import tkinter.messagebox
from PIL import Image, ImageTk
from fastcore.all import concat
import torch, logging
from pathlib import Path
from huggingface_hub import notebook_login
from diffusers import StableDiffusionPipeline
from PIL import Image
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter import *
from tkinter import font
from random import choice

torch.manual_seed(1)
if not (Path.home()/'.huggingface'/'token').exists(): notebook_login()

model_string_v1 = 'CompVis/stable-diffusion-v1-4'
model_string_v2 = 'stabilityai/stable-diffusion-2-1-base'
pipe = StableDiffusionPipeline.from_pretrained(model_string_v2, revision="fp16", torch_dtype=torch.float16).to("cuda")

art_styles = ["anime", "oil painting", "drawing","water color painting" "cartoon", "digital illustration", "disney animation studios", "pixar 3-d animation"]
genres = ["steampunk", "sciene fiction", "film noir", "fantasy", "90s", "80s", "70s", "60s", "50s", "western"]
pallettes = ["cool colors", "warm colors", "sepia", "black and white", "cell shaded"]
misc_parameters = ["rule of threes", "golden ratio", "4k resolution", "trending on deviantart"]

def image_gen(prompt):
    pipe.enable_attention_slicing()
    results = pipe(prompt= f"{choice(misc_parameters)}, prompt , {choice(art_styles)}, {choice(genres)}, {pallettes}, {choice(misc_parameters)}", 
               height=None, width=None, num_inference_steps=50, guidance_scale=7.5, 
               num_images_per_prompt=1, output_type='pil', return_dict=True, callback=None,
               negative_prompt= """mutilated fingers, twisted fingers, deformed fingers, racism, sexism, homophobia, china, chinese, communism,
               communist party, xi jinping, mao zedong, han chinese, taiwan, kmt, guomindang, kuomintang, penis, vagina, human genetalia, sex, murder, rape,
               tibet, pixellated, pixellation, blur, blurry, static, non-objective, abstract, tian'an men square, hong kong, protest, covid, covid-19,
               xinjiang, uyghur, uighur, muslim, islam, islamic, slaves, slavery, israel, jews, holocaust""")
    
    return results.images

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
    
    result = generator(prompt,min_length=175, max_length=225 , do_sample=True, temperature=0.89)
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