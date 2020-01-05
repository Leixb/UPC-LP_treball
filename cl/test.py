import sys

from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from EnquestesVisitor import EnquestesVisitor
from antlr4.InputStream import InputStream

import matplotlib.pyplot as plt
import networkx as nx

if len(sys.argv) > 1:
    input_stream = FileStream(sys.argv[1], encoding='utf-8')

else:
    input_stream = InputStream(input('? '))
lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()

visitor = EnquestesVisitor()
print(visitor.visit(tree))

#nx.draw_circular(visitor.G, with_labels=True)

G = visitor.G

pos = nx.circular_layout(G)
plt.figure()
nx.draw(G, pos, edge_color='black', width=1,linewidths=1,\
node_size=500, node_color='pink', alpha=0.9,\
labels={node:node for node in G.nodes()})
nx.draw_networkx_edge_labels(G,pos,edge_labels=visitor.edge_labels, font_color='red')

plt.axis('off')
plt.savefig('foo.png')

#print(tree.toStringTree(recog=parser))
