#!/usr/bin/env python3

import networkx as nx

from antlr4 import ParseTreeVisitor

if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser


class EnquestesVisitor(ParseTreeVisitor):
    def __init__(self):
        self.G = nx.DiGraph()
        self.add_node("END", tipus="END")
        self.items = dict()

    def add_node(self, node: str, **kwargs):
        self.G.add_node(node, **kwargs)

    def add_edge(self, a: str, b: str, **kwargs):
        self.G.add_edge(a, b, **kwargs)

    def id_preg(self, id_item):
        return self.items[id_item][0]

    # Visit a parse tree produced by EnquestesParser#root.
    def visitRoot(self, ctx: EnquestesParser.RootContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]

        for i in l[:-1]:
            self.visit(i)

        return self.G

    # Visit a parse tree produced by EnquestesParser#enquesta.
    def visitEnquesta(self, ctx: EnquestesParser.EnquestaContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        return [self.visit(i) for i in l[:-2]]

    # Visit a parse tree produced by EnquestesParser#preg.
    def visitPreg(self, ctx: EnquestesParser.PregContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        ident = self.visit(l[0])
        text = self.visit(l[4])

        self.add_node(ident, tipus="pregunta", text=text)

    # Visit a parse tree produced by EnquestesParser#text_pregunta.
    def visitText_pregunta(self, ctx: EnquestesParser.Text_preguntaContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [str(next(g)) for i in range(n_children)]
        return " ".join(l)

    # Visit a parse tree produced by EnquestesParser#resp.
    def visitResp(self, ctx: EnquestesParser.RespContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]

        ident = self.visit(l[0])
        opcions = self.visit(l[4])
        self.add_node(ident, tipus="resposta", opcions=opcions)

    # Visit a parse tree produced by EnquestesParser#opcions_resposta.
    def visitOpcions_resposta(self, ctx: EnquestesParser.Opcions_respostaContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [self.visit(next(g)) for i in range(n_children)]
        return l

    # Visit a parse tree produced by EnquestesParser#opcio_resposta.
    def visitOpcio_resposta(self, ctx: EnquestesParser.Opcio_respostaContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        return {"id": self.visit(l[0]), "text": self.visit(l[2])}

    # Visit a parse tree produced by EnquestesParser#text_opcio.
    def visitText_opcio(self, ctx: EnquestesParser.Text_opcioContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [str(next(g)) for i in range(n_children)]
        text = " ".join(l)
        return text.split(";")[0].strip()

    # Visit a parse tree produced by EnquestesParser#id_opcio.
    def visitId_opcio(self, ctx: EnquestesParser.Id_opcioContext):
        g = ctx.getChildren()
        return int(next(g).getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by EnquestesParser#item.
    def visitItem(self, ctx: EnquestesParser.ItemContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        ident = self.visit(l[0])
        id_preg = self.visit(l[4])
        id_resp = self.visit(l[6])
        edge = (id_preg, id_resp)

        self.add_edge(*edge, id=ident, tipus="item")
        self.items[ident] = edge

    # Visit a parse tree produced by EnquestesParser#id_preg.
    def visitId_preg(self, ctx: EnquestesParser.Id_pregContext):
        return ctx.getText()

    # Visit a parse tree produced by EnquestesParser#id_resp.
    def visitId_resp(self, ctx: EnquestesParser.Id_respContext):
        return ctx.getText()

    # Visit a parse tree produced by EnquestesParser#alte.
    def visitAlte(self, ctx: EnquestesParser.AlteContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]

        ident = self.visit(l[0])
        id_item = self.visit(l[4])
        alternatives = self.visit(l[5])

        id_pregunta = self.items[id_item][0]

        for i in alternatives:
            edge = (id_pregunta, self.id_preg(i["id_item"]))
            self.add_edge(*edge, id_opcio=i["id_opcio"], tipus="alternativa")

    # Visit a parse tree produced by EnquestesParser#alternatives.
    def visitAlternatives(self, ctx: EnquestesParser.AlternativesContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        l = l[1:-1]
        return [self.visit(i) for i in l]

    # Visit a parse tree produced by EnquestesParser#alternativa.
    def visitAlternativa(self, ctx: EnquestesParser.AlternativaContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]

        return {"id_opcio": self.visit(l[1]), "id_item": self.visit(l[3])}

    # Visit a parse tree produced by EnquestesParser#enqu.
    def visitEnqu(self, ctx: EnquestesParser.EnquContext):
        n_children = ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        ident = self.visit(l[0])

        items = [self.visit(i) for i in l[4:-1]]

        self.add_node(ident, tipus="enquesta")

        def add_edge_enq(u, v):
            edge = (u, v)
            llista_enq = [ident]
            if self.G.has_edge(*edge):
                llista_enq = self.G.get_edge_data(*edge)["id_enq"] + [ident]
            self.add_edge(*edge, tipus="default", id_enq=llista_enq)

        prev = items[0]
        add_edge_enq(ident, self.id_preg(prev))
        for i in items[1:]:
            add_edge_enq(self.id_preg(prev), self.id_preg(i))
            prev = i
        add_edge_enq(self.id_preg(prev), "END")

    # Visit a parse tree produced by EnquestesParser#identificador.
    def visitIdentificador(self, ctx: EnquestesParser.IdentificadorContext):
        return ctx.getText()


del EnquestesParser
