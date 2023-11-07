import ijson
import simplejson as json
import itertools
import os
from tqdm import tqdm

INPUT_PATH = "data/input/netflow/attack_2.json"
OUTPUT_DIR = "data/input/netflow/attack_2/"

# Define a function to read the JSON file in chunks
def read_json_in_chunks(file_path, chunk_size=10000):
    with open(file_path, "r") as f:
        items = ijson.items(f, "item")
        while True:
            chunk = list(itertools.islice(items, chunk_size))
            if not chunk:
                break
            yield chunk

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Iterate through the chunks and process each chunk
for i, chunk in enumerate(read_json_in_chunks(INPUT_PATH)):
    print(i, end="\r")
    output_path = os.path.join(OUTPUT_DIR, f"{i}.json")
    with open(output_path, "w+") as f:
        f.write(json.dumps(chunk, use_decimal=True))
    
