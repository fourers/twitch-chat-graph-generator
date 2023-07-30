import json


def get_json_data(file_path: str, limit: int = 0) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as file:
        chat_json = json.load(file)
    chat_data = chat_json["comments"]
    if limit > 0:
        return chat_data[:limit]
    return chat_data
