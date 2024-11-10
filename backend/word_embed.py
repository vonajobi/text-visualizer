from transformers import BertModel, BertTokenizer
import torch

EMBEDDED_CACHE = {}
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

def get_word_embedding(word: str)->torch.Tensor:
    if word in EMBEDDED_CACHE:
        return EMBEDDED_CACHE[word]
    else:
        inputs = tokenizer(word, return_tensors='pt')

        with torch.no_grad():
            outputs = model(**inputs)

        word_embed = outputs.last_hidden_state.mean(dim=1).squeeze()
        EMBEDDED_CACHE[word]=(word_embed)

        return word_embed
