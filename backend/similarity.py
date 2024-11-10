from sklearn.metrics.pairwise import cosine_similarity
from word_embed import get_word_embedding
from typing import List, Dict, Union
import os, json
from files import *

def write_file( file_path: str, entry: Dict[str, Union[str, float]])-> None:
    if not os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load()
    else: 
        data = []

    data.append(entry)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def read_file(file_path: str) -> List[Dict[str, Union[str, float]]]:
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([], f)

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)



def calc_similarity(word1: str, word2: str)-> float:
    sample_cache = read_file(SIMILARITY_EDGE_FILE_PATH)
    if (word1, word2) in sample_cache:
        return sample_cache[(word1, word2)]
    if(word2, word1) in sample_cache:
        return sample_cache[(word2, word1)]

    embedd1 = get_word_embedding(word1)
    embedd2 = get_word_embedding(word2)

    for d in read_file(sample_cache):
        sample_cache.append({(d['word1'], d['word2']): d['similarity']})


    similarity_score = cosine_similarity(embedd1.reshape(1,-1).numpy(),
                                   embedd2.reshape(1,-1).numpy()
                                   )[0][0]
    write_file(SIMILARITY_EDGE_FILE_PATH, {'word1': word1, 'word2': word2, 'similarity': similarity_score})

    return similarity_score

# read data.json file which contains each word as a node
# read similarites.json which represents the links
def get_most_similar_words(new_node: str, top_n=10)-> List[Dict[str, Union[str, float]]]:  
    similarities = []

    node_list = read_file(NODE_FILE_PATH)
    for dict in node_list:
        if new_node not in dict:
            write_file(NODE_FILE_PATH, {'word': new_node})

            for node in node_list:
                existing_word = node['word']
                if existing_word != new_node:                        # if the val in the key val pair not equal the new word
                    similarity = calc_similarity(new_node, existing_word)
                    similarities.append((existing_word, similarity))           
                    write_file(SIMILARITY_EDGE_FILE_PATH, {'word1': new_node, 'word2': existing_word, 'similarity': similarity})
        
        sorted_similar_w = sorted(similarities, key=lambda x:x[1], reverse=True)[:top_n]
        result = []
        for w, score in sorted_similar_w:
            result.append({'word': w, 'similarity': round(score, 3)})

    return result

