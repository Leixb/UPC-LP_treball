import sys

from antlr4 import *
from EnquestesLexer import EnquestesLexer
from EnquestesParser import EnquestesParser
from EnquestesVisitor import EnquestesVisitor
from antlr4.InputStream import InputStream

if len(sys.argv) > 1:
    input_stream = FileStream(sys.argv[1], encoding='utf-8')

else:
    input_stream = InputStream(input('? '))
lexer = EnquestesLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = EnquestesParser(token_stream)
tree = parser.root()

visitor = EnquestesVisitor()
print("JAMES")
print(visitor.visit(tree))
print("PTOTA")

#print(tree.toStringTree(recog=parser))
