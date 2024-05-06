import json
from pathlib import Path


def load_output_json(input_dir: Path):
    try:
        output_json_path = input_dir / "output.json"
        with open(output_json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"no output.json file in: {input_dir.absolute()}")
