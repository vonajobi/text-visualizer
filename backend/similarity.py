from sklearn.metrics.pairwise import cosine_similarity
from word_embed import get_word_embedding
from typing import List, Dict, Union
import os, json
from files import DATA_FILE_PATH
import logging



def write_file( file_path: str, data: Dict[str, Union[List[Dict[str, str]], Dict[str, float]]])-> None:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def read_file(file_path: str) -> Dict[str, Union[List[Dict[str, str]], Dict[str, float]]]:
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"nodes": [],"similarities": {}}, f)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"nodes": [], "similarities": {}}

def get_data()-> Dict[str, Union[List[Dict[str, str]], Dict[str, float]]]:
    return read_file(DATA_FILE_PATH)


def add_similarity(word1: str, word2: str, similarity: float) -> None:
    data = get_data()
    key = f"{min(word1, word2)}_{max(word1, word2)}"
    data["similarities"][key] = round(float(similarity), 5)
    write_file(DATA_FILE_PATH, data)


def add_node(word: str) -> None:
    data = get_data()
    data["nodes"].append({"word": word})
    write_file(DATA_FILE_PATH, data)


def calc_similarity(word1: str, word2: str)-> float:
    sample_cache = get_data()
    similarities = sample_cache["similarities"]

    key = f"{min(word1, word2)}_{max(word1, word2)}"
    if key in similarities:
        return similarities[key]

    embedd1 = get_word_embedding(word1)
    embedd2 = get_word_embedding(word2)

    similarity_score = cosine_similarity(embedd1.reshape(1,-1).numpy(),
                                   embedd2.reshape(1,-1).numpy()
                                   )[0][0]
    add_similarity(word1, word2, similarity_score)

    return float(similarity_score)

# read data.json file which contains each word as a node
# read similarites.json which represents the links
def get_most_similar_words(new_node: str, top_n: int=10)-> List[Dict[str, Union[str, float]]]:  

    data = get_data()
    node_list = data["nodes"]
    similarities = data["similarities"]
    # Check if the new node already exists
    if not any(node['word'] == new_node for node in node_list):
        add_node(new_node)

        for node in node_list:
            existing_word = node['word']
            if existing_word != new_node:
                similarity = calc_similarity(new_node, existing_word)
                # json doesnt allow tuples womp womp :/
                key = f"{min(new_node, existing_word)}_{max(new_node, existing_word)}"
                similarities[key] = similarity
                logger.debug(f"Calculated similarity between {new_node} and {existing_word}: {similarity}")

        data["similarities"] = similarities
        write_file(DATA_FILE_PATH, data)
    similar_words = [
        
        {"word": word_pair.split('_')[1], "similarity": round(score, 5)}
        for word_pair, score in similarities.items()
        if new_node in word_pair
    ]
    sorted_similar_words = sorted(similar_words, key=lambda x: x["similarity"], reverse=True)[:top_n]
    return sorted_similar_words

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# if __name__ == '__main__':
#     test_word = "Earth"
    
#     sample = get_most_similar_words(test_word)
#     if not sample:
#         print('error')
    
