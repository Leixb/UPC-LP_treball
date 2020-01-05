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


def main():

    if len(sys.argv) > 1:
        input_stream = FileStream(sys.argv[1], encoding="utf-8")
    else:
        input_stream = InputStream(input("? "))

    graph = parse_to_network(input_stream)

    save_pickle(graph, PICKLE_FILE)
    G = read_pickle(PICKLE_FILE)

    plot_network(G, PLOT_FILE)


def parse_to_network(input_stream) -> nx.DiGraph:
    lexer = EnquestesLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = EnquestesParser(token_stream)
    tree = parser.root()

    visitor = EnquestesVisitor()
    return visitor.visit(tree)


def read_pickle(filename: str) -> nx.DiGraph:
    with open(filename, "rb") as file:
        return pickle.load(file)


def save_pickle(G: nx.DiGraph, filename: str):
    with open(filename, "wb") as file:
        pickle.dump(G, file)


def plot_network(G: nx.DiGraph, filename: str):

    pos = nx.circular_layout(G)
    plt.figure()

    nx.draw(
        G,
        pos,
        edge_color="black",
        width=1,
        linewidths=1,
        node_size=500,
        node_color="pink",
        alpha=0.9,
        labels={node: node.id for node in G.nodes()},
    )

    edge_labels = nx.get_edge_attributes(G, "id")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    edge_labels_opcio = nx.get_edge_attributes(G, "id_opcio")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels_opcio, font_color="blue"
    )

    plt.axis("off")
    plt.savefig(filename)


if __name__ == "__main__":
    main()

# print(tree.toStringTree(recog=parser))
