import datetime
from dataclasses import dataclass
from statistics import mean
from typing import Optional

from tqdm import tqdm

from chat.colours import convert_rgb_to_colour, convert_colour_to_name


@dataclass(frozen=True)
class ChatEdge:
    pair: tuple[int, int]
    weight: float


class ChatProximity:

    def __init__(self, threshold: float):
        self._data: dict[tuple[int, int], list[float]] = {}
        self._threshold = threshold

    def add_proximity(self, user1: int, user2: int, proximity: float):
        if user1 == user2:
            raise KeyError("Same user ids")
        if proximity > self._threshold:
            raise ValueError("Invalid proximity")
        if user2 < user1:
            user1, user2 = user2, user1
        pair = (user1, user2)
        if pair not in self._data:
            self._data[pair] = [proximity]
        else:
            self._data[pair].append(proximity)

    @property
    def data(self) -> list[ChatEdge]:
        return [ChatEdge(k, mean(v)) for k, v in tqdm(self._data.items())]


class ChatMessage:

    @staticmethod
    def convert_hex_to_colour(hex_code: Optional[str]):
        if hex_code is None:
            hex_code = "#808080"
        return convert_rgb_to_colour(hex_code)

    def __init__(self, data: dict):
        self._data = data
        self.chat_id = data["_id"]
        self.user_id = data["commenter"]["_id"]
        self.username = data["commenter"]["name"]
        self.user_colour = self.convert_hex_to_colour(data["message"]["user_color"])
        self.timestamp = datetime.datetime.fromisoformat(data["created_at"])
        self.rounded_timestamp = self.timestamp.replace(second=0, microsecond=0)

    @property
    def colour(self):
        return convert_colour_to_name(self.user_colour)


def convert_to_chat_messages(data: list[dict]) -> list[ChatMessage]:
    return [ChatMessage(msg) for msg in data]


@dataclass(frozen=True)
class ChatNode:
    user_id: int
    label: str
    count: int
    colour: str


class ChatNodes:

    def __init__(self):
        self._data = {}

    def update_node(self, user_id: int, username: str, user_colour: str, colour: str):
        data = {
            "label": username,
            "count": self._data.get(user_id, {}).get("count", 0) + 1,
            "user_colour": user_colour,
            "colour": colour,
        }
        self._data[user_id] = data

    @property
    def data(self) -> list[ChatNode]:
        return [ChatNode(k, v["label"], v["count"], v["colour"]) for k, v in tqdm(self._data.items())]