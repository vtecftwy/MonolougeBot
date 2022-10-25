from happytransformer import HappyGeneration
from happytransformer import GENSettings

happy_gen = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-125M", load_path= "MonolougeBotModel2/")
top_k_sampling_settings = GENSettings(no_repeat_ngram_size=2, min_length = 200, max_length = 300, do_sample=True, early_stopping=False,top_p=1.0, top_k=50, temperature=1.0, bad_words= ["nigger","niggers","niggas", "nigga", "fag", "faggot", "chink","dyke", "kike", "jew", "jews", "retard", "retards", "communist", "communists", "CCP", "China", "Chinese","COVID","Xinjiang","Taiwan","Pelosi","Ukraine","Russia"] )
prompt = input("What's on your mind?: ")
result = happy_gen.generate_text(prompt, args=top_k_sampling_settings)
print(f"{prompt}{result.text}")