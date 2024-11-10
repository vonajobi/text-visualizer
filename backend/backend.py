from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import lru_cache
from similarity import *
from files import NODE_FILE_PATH

app = Flask(__name__)
CORS(app)

# sample vocab, change out to Hollow Craft json file
# sample_vocab = ['example', 'sample', 'demonstration', 'illustration', 'test', 'trial', 'Figma', 'pattern', 'web-dev']

node_list = read_file(NODE_FILE_PATH)
sample_vocab = [node['word'] for node in node_list]

@lru_cache(maxsize=500)
@app.route('/similar_words', methods=['GET'])
def similar_words():
    word = request.args.get('word')
    if not word:
        return jsonify({'error':'Provide a word'}), 400

    # sample vocab is a list containg all the node words

    if not sample_vocab:
        return jsonify({'error': 'Vocabularay is empty'}), 404
    elif word not in sample_vocab:
        return jsonify({'error': f'Word {word} not found in vocabularay'}), 404

    result = get_most_similar_words(word, sample_vocab)
    if not result:
        return jsonify({'message': f'No similar word found for {word}'}), 200

    return jsonify(result)

@app.route('/add_word', methods=['POST'])
def add_word():
    new_word = request.json['word']
    if not new_word:
        return jsonify({'error': 'No word provided'}), 400
    if new_word not in sample_vocab:
        sample_vocab.append(new_word)
    
    simi_score = get_most_similar_words(new_word, sample_vocab)
    return jsonify({'mesage': f'{new_word.capitalize()} added'})

@app.route('/get_network_data', methods=['GET'])
def get_network_data():
    similarities = read_file(SIMILARITY_EDGE_FILE_PATH)
    nodes = [{'id': word} for word in sample_vocab]
    links = []
    for similarity in similarities:
        links.append({'source': similarity['word1'],
                       'target': similarity['word2'], 
                       'score': similarity['score']})

    return jsonify({'nodes': nodes, 'links': links})

if __name__ == '__main__':
    app.run(debug=True)
