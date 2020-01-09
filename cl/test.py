#!/usr/bin/env python3

import sys
import pickle

import matplotlib.pyplot as plt
import networkx as nx

from antlr4 import FileStream, CommonTokenStream
from antlr4.InputStream import InputStream

from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from EnquestesVisitor import EnquestesVisitor


PICKLE_FILE = "network_graph.pckl"
PLOT_FILE = "network_graph.png"

plt.ioff()

def main():
    """Funcio principal, inicialitza l'entrada, guarda en un pickle i genera una gràfica."""

    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding="utf-8")
    else:
        input_stream = InputStream(input("? "))

    graph = parse_to_network(input_stream)

    save_pickle(graph, PICKLE_FILE)
    graph_restored = read_pickle(PICKLE_FILE)

    plot_network(graph_restored, PLOT_FILE)


def parse_to_network(input_stream) -> nx.DiGraph:
    """Parseja i retorna el graph."""
    lexer = EnquestesLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = EnquestesParser(token_stream)
    tree = parser.root()

    visitor = EnquestesVisitor()
    return visitor.visit(tree)


def read_pickle(filename: str) -> nx.DiGraph:
    """Recupera el graph del pickle."""
    with open(filename, "rb") as file:
        return pickle.load(file)


def save_pickle(graph: nx.DiGraph, filename: str):
    """Guarda el graph a un pickle."""
    with open(filename, "wb") as file:
        pickle.dump(graph, file)


def plot_network(graph: nx.DiGraph, filename: str):
    """Genera i guarda la gràfica del arbre."""

    pos = nx.circular_layout(graph)
    plt.figure()

    draw_nodes(graph, pos, "pregunta", "deepskyblue")
    draw_nodes(graph, pos, "resposta", "khaki")
    draw_nodes(graph, pos, "enquesta", "lightgreen")
    draw_nodes(graph, pos, "END", "pink")

    node_labels = {node: node for node in graph.nodes()}
    nx.draw_networkx_labels(graph, pos, labels=node_labels)

    draw_edges(graph, pos, "id", "blue")
    draw_edges(graph, pos, "id_opcio", "green")
    draw_edges(graph, pos, "id_enq", "black")

    plt.axis("off")
    plt.savefig(filename)


def draw_edges(graph: nx.DiGraph, pos, attr: str, color: str, **kwargs):
    """Draws graph edges that have the given attribute."""
    edge_labels = nx.get_edge_attributes(graph, attr)
    edge_labels = {k: flatten(v) for k, v in edge_labels.items()}
    nx.draw_networkx_edges(
        graph, pos, edgelist=edge_labels.keys(), edge_color=color, **kwargs
    )
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color=color)


def flatten(obj):
    if not isinstance(obj, list):
        return obj
    return ",".join(obj)


def draw_nodes(graph: nx.DiGraph, pos, tipus: str, color: str, **kwargs):
    """Draws graph nodes that have the given "tipus"."""
    node_list = [
        n for n, d in graph.nodes(data=True) if "tipus" in d and d["tipus"] == tipus
    ]
    nx.draw_networkx_nodes(graph, pos, nodelist=node_list, node_color=color, **kwargs)


if __name__ == "__main__":
    main()
