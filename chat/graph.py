import datetime
import time
from functools import lru_cache

from networkx import Graph, write_gexf
from tqdm import tqdm

from chat.constants import PROXIMITY_MINUTES_THRESHOLD, EDGE_WEIGHT_THRESHOLD
from chat.model import ChatMessage, ChatNode, ChatNodes, ChatEdge, ChatProximity


def generate_nodes(chat_messages: list[ChatMessage]) -> list[ChatNode]:
    chat_nodes = ChatNodes()
    for message in tqdm(chat_messages):
        chat_nodes.update_node(
            message.user_id, message.username, message.user_colour, message.colour
        )
    return chat_nodes.data


class MessageCache:
    def __init__(self, chat_messages: list[ChatMessage]):
        self._chat_messages = chat_messages

    @lru_cache
    def filter(self, rounded_timestamp: datetime.datetime) -> list[ChatMessage]:
        return [
            msg
            for msg in self._chat_messages
            if abs((msg.timestamp - rounded_timestamp).total_seconds() / 60)
            < PROXIMITY_MINUTES_THRESHOLD + 1
        ]


def generate_edges(chat_messages: list[ChatMessage]) -> list[ChatEdge]:
    chat_model = ChatProximity(PROXIMITY_MINUTES_THRESHOLD)
    message_filter = MessageCache(chat_messages)
    for message in tqdm(chat_messages):
        for iter_message in message_filter.filter(message.rounded_timestamp):
            if message.username == iter_message.username:
                continue
            minutes_difference = abs(
                (message.timestamp - iter_message.timestamp).total_seconds() / 60
            )
            if minutes_difference < PROXIMITY_MINUTES_THRESHOLD:
                chat_model.add_proximity(
                    message.user_id,
                    iter_message.user_id,
                    PROXIMITY_MINUTES_THRESHOLD - minutes_difference,
                )
    return chat_model.data


def generate_network_graph(
    nodes: list[ChatNode],
    edges: list[ChatEdge],
) -> Graph:
    graph = Graph()
    for node in tqdm(nodes):
        graph.add_node(node.user_id, label=node.label, count=node.count)
    for edge in tqdm(edges):
        if edge.weight > EDGE_WEIGHT_THRESHOLD:
            graph.add_edge(*edge.pair, weight=edge.weight)
    print(f"Created graph with {len(graph.nodes)} nodes and {len(graph.edges)} edges")
    return graph


def write_gexf_file(graph: Graph, output_file_path: str) -> None:
    output_file_name = f"{output_file_path.rstrip('/')}/{int(time.time())}.gexf"
    write_gexf(graph, output_file_name)
    print(f"Output to: {output_file_name}")
