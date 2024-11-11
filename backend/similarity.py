from sklearn.metrics.pairwise import cosine_similarity
from word_embed import get_word_embedding
from typing import List, Dict, Union
from write_data import *
from files import DATA_FILE_PATH
import logging



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


def get_neighbors(word: str, top_n: int = 5) -> List[str]:
    data = get_data()
    node_list = data["nodes"]
    sample_vocab = [node['word'] for node in node_list if 'word' in node]

    embedd1 = get_word_embedding(word)
    similarities = []

    for w in sample_vocab:
        if w != word:
            embedd2 = get_word_embedding(w)
            similarity_score = cosine_similarity(embedd1.reshape(1, -1).numpy(), embedd2.reshape(1, -1).numpy())[0][0]
            similarities.append((w, similarity_score))

    # Sort by similarity score and select top_n neighbors
    similarities.sort(key=lambda x: x[1], reverse=True)
    neighbors = [w for w, _ in similarities[:top_n]]
    return neighbors

def initialize_similarities(top_n: int = 5) -> None:
    data = get_data()
    node_list = data["nodes"]
    similarities = data.get("similarities", {})

    for node in node_list:
        word = node['word']
        neighbors = get_neighbors(word, top_n)
        for neighbor in neighbors:
            key = f"{min(word, neighbor)}_{max(word, neighbor)}"
            if key not in similarities:
                embedd1 = get_word_embedding(word)
                embedd2 = get_word_embedding(neighbor)
                similarity_score = cosine_similarity(embedd1.reshape(1, -1).numpy(), embedd2.reshape(1, -1).numpy())[0][0]
                similarity = float(round(similarity_score, 5))
                similarities[key] = similarity
                logger.debug(f"Calculated similarity between {word} and {neighbor}: {similarity}")

    data["similarities"] = similarities
    write_file(DATA_FILE_PATH, data)


def calc_similarity(word: str, top_n: int = 3) -> List[Dict[str, Union[str, float]]]:
    data = get_data()
    similarities = data["similarities"]

    neighbors = get_neighbors(word, top_n)
    new_similarities = []

    for neighbor in neighbors:
        key = f"{min(word, neighbor)}_{max(word, neighbor)}"
        if key in similarities:
            similarity = similarities[key]
        else:
            embedd1 = get_word_embedding(word)
            embedd2 = get_word_embedding(neighbor)
            similarity_score = cosine_similarity(embedd1.reshape(1, -1).numpy(), embedd2.reshape(1, -1).numpy())[0][0]
            similarity = float(round(similarity_score, 5))
            add_similarity(word, neighbor, similarity)
        new_similarities.append({'word': neighbor, 'similarity': similarity})

    return new_similarities

# read data.json file which contains each word as a node
# read similarites.json which represents the links
def get_most_similar_words(new_node: str, top_n: int=3)-> List[Dict[str, Union[str, float]]]:  

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

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    initialize_similarities()
    
