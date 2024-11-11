from typing import List, Dict, Union
import os, json


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
    
def read_coordinates(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_coordinates(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


