import glob

from chat.graph import (
    generate_nodes,
    generate_edges,
    generate_network_graph,
    write_gexf_file,
)
from chat.model import convert_to_chat_messages
from chat.parser import get_json_data


def main():
    chat_messages = []
    for file_path in glob.glob("data/*.json"):
        chat_json = get_json_data(file_path)
        chat_messages.extend(convert_to_chat_messages(chat_json))

    nodes = generate_nodes(chat_messages)
    edges = generate_edges(chat_messages)
    graph = generate_network_graph(nodes, edges)
    write_gexf_file(graph, "output")


if __name__ == "__main__":
    main()
