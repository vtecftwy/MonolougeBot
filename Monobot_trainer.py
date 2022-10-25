from happytransformer import HappyGeneration
from happytransformer import GENTrainArgs
import torch
import os
os.environ['PYTORCH_CUDA_ALLOC_CONF']='max_split_size_mb':128

happy_gen = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-125M")
args = GENTrainArgs(num_train_epochs=1)
happy_gen.train("train.txt", args=args)
torch.cuda.empty_cache()
happy_gen.save("MonolougeBotModel3/")