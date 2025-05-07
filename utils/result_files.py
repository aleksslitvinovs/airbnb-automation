import json
import os
import re
from typing import Any


def save_json_to_file(filename: str, content: dict[str, Any]) -> None:
    """
    Saves JSON content to a file.

    Args:
        file_path (str): The path to the file where the JSON content will be saved.
        content (dict): The JSON content to save.

    Returns:
        None
    """

    normalized_filename = re.sub(r"[^a-zA-Z0-9_-]", "", filename.lower())

    os.makedirs("temp", exist_ok=True)
    with open(os.path.join("temp", f"{normalized_filename}.json"), "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)
