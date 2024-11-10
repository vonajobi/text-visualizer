import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import lru_cache
from similarity import get_most_similar_words, read_file, write_file, get_data, add_node
from files import DATA_FILE_PATH

app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.DEBUG)

@app.route('/similar_words', methods=['GET'])
def similar_words():
    word = request.args.get('word')
    if not word:
        return jsonify({'error': 'Provide a word'}), 400

    data = get_data()
    node_list = data["nodes"]
    sample_vocab = [node['word'] for node in node_list if 'word' in node]
    app.logger.debug(f"Sample vocab: {sample_vocab}")

    if not sample_vocab:
        app.logger.debug(f"{DATA_FILE_PATH}, {sample_vocab}")
        return jsonify({'error': 'Vocabulary is empty'}), 404
    elif word not in sample_vocab:
        return jsonify({'error': f'Word {word} not found in vocabulary'}), 404

    result = get_most_similar_words(word)
    if not result:
        return jsonify({'message': f'No similar word found for {word}'}), 200

    return jsonify(result)

@app.route('/add_word', methods=['POST'])
def add_word():
    new_word = request.json['word']
    if not new_word:
        return jsonify({'error': 'No word provided'}), 400

    data = get_data()
    node_list = data["nodes"]
    sample_vocab = [node['word'] for node in node_list if 'word' in node]

    if new_word not in sample_vocab:
        add_node(new_word)
        app.logger.debug(f"Added new word: {new_word}")

    return jsonify({'message': f'Word {new_word} added successfully'})

@app.route('/get_network_data', methods=['GET'])
def get_network_data():
    data = get_data()
    nodes = [{'id': node['word']} for node in data['nodes']]
    links = []
    for key, value in data['similarities'].items():
        source, target = key.split('_')
        link = {
            'source': source,
            'target': target,
            'value': value
        }
        links.append(link)
    return jsonify({'nodes': nodes, 'links': links})

if __name__ == '__main__':
    app.run(debug=True)
