#!/usr/bin/env python3

import networkx as nx

from antlr4 import ParseTreeVisitor

from EnquestesParser import EnquestesParser


class EnquestesVisitor(ParseTreeVisitor):
    """Visitor de Enquestes"""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.graph.add_node("END", tipus="END")
        self.items = dict()

    def __id_preg(self, id_item):
        return self.items[id_item][0]

    @staticmethod
    def __get_children_list(ctx):
        n_children = ctx.getChildCount()
        children = ctx.getChildren()
        return [next(children) for _ in range(n_children)]

    def visitRoot(self, ctx: EnquestesParser.RootContext):
        """Visit a parse tree produced by EnquestesParser#root."""

        for i in self.__get_children_list(ctx)[:-1]:
            self.visit(i)

        return self.graph

    def visitEnquesta(self, ctx: EnquestesParser.EnquestaContext):
        """Visit a parse tree produced by EnquestesParser#enquesta."""
        return [self.visit(i) for i in self.__get_children_list(ctx)[:-2]]

    def visitPreg(self, ctx: EnquestesParser.PregContext):
        """Visit a parse tree produced by EnquestesParser#preg."""
        children = self.__get_children_list(ctx)
        ident = self.visit(children[0])
        text = self.visit(children[4])

        self.graph.add_node(ident, tipus="pregunta", text=text)

    def visitText_pregunta(self, ctx: EnquestesParser.Text_preguntaContext):
        """Visit a parse tree produced by EnquestesParser#text_pregunta."""
        children = [str(i) for i in self.__get_children_list(ctx)]
        return " ".join(children)

    def visitResp(self, ctx: EnquestesParser.RespContext):
        """Visit a parse tree produced by EnquestesParser#resp."""
        children = self.__get_children_list(ctx)

        ident = self.visit(children[0])
        opcions = self.visit(children[4])
        self.graph.add_node(ident, tipus="resposta", opcions=opcions)

    def visitOpcions_resposta(self, ctx: EnquestesParser.Opcions_respostaContext):
        """Visit a parse tree produced by EnquestesParser#opcions_resposta."""
        return [self.visit(i) for i in self.__get_children_list(ctx)]

    def visitOpcio_resposta(self, ctx: EnquestesParser.Opcio_respostaContext):
        """Visit a parse tree produced by EnquestesParser#opcio_resposta."""
        children = self.__get_children_list(ctx)
        return {"id": self.visit(children[0]), "text": self.visit(children[2])}

    def visitText_opcio(self, ctx: EnquestesParser.Text_opcioContext):
        """Visit a parse tree produced by EnquestesParser#text_opcio."""
        children = [str(i) for i in self.__get_children_list(ctx)]
        text = " ".join(children)
        return text.split(";")[0].strip()

    def visitId_opcio(self, ctx: EnquestesParser.Id_opcioContext):
        """Visit a parse tree produced by EnquestesParser#id_opcio."""
        return int(next(ctx.getChildren()).getText())

    def visitItem(self, ctx: EnquestesParser.ItemContext):
        """Visit a parse tree produced by EnquestesParser#item."""
        children = self.__get_children_list(ctx)
        ident = self.visit(children[0])
        id_preg = self.visit(children[4])
        id_resp = self.visit(children[6])
        edge = (id_preg, id_resp)

        self.graph.add_edge(*edge, id=ident, tipus="item")
        self.items[ident] = edge

    def visitId_preg(self, ctx: EnquestesParser.Id_pregContext):
        """Visit a parse tree produced by EnquestesParser#id_preg."""
        return ctx.getText()

    def visitId_resp(self, ctx: EnquestesParser.Id_respContext):
        """Visit a parse tree produced by EnquestesParser#id_resp."""
        return ctx.getText()

    def visitAlte(self, ctx: EnquestesParser.AlteContext):
        """Visit a parse tree produced by EnquestesParser#alte."""
        children = self.__get_children_list(ctx)

        ident = self.visit(children[0])
        id_item = self.visit(children[4])
        alternatives = self.visit(children[5])

        id_pregunta = self.items[id_item][0]

        for i in alternatives:
            edge = (id_pregunta, self.__id_preg(i["id_item"]))
            self.graph.add_edge(*edge, id_opcio=i["id_opcio"], tipus="alternativa")

    def visitAlternatives(self, ctx: EnquestesParser.AlternativesContext):
        """Visit a parse tree produced by EnquestesParser#alternatives."""
        return [self.visit(i) for i in self.__get_children_list(ctx)[1:-1]]

    def visitAlternativa(self, ctx: EnquestesParser.AlternativaContext):
        """Visit a parse tree produced by EnquestesParser#alternativa."""
        children = self.__get_children_list(ctx)

        return {"id_opcio": self.visit(children[1]), "id_item": self.visit(children[3])}

    def visitEnqu(self, ctx: EnquestesParser.EnquContext):
        """Visit a parse tree produced by EnquestesParser#enqu."""
        children = self.__get_children_list(ctx)
        ident = self.visit(children[0])

        items = [self.visit(i) for i in children[4:-1]]

        self.graph.add_node(ident, tipus="enquesta")

        def add_edge_enq(u, v):
            edge = (u, v)
            llista_enq = [ident]
            if self.graph.has_edge(*edge):
                llista_enq = self.graph.get_edge_data(*edge)["id_enq"] + [ident]
            self.graph.add_edge(*edge, tipus="default", id_enq=llista_enq)

        prev = items[0]
        add_edge_enq(ident, self.__id_preg(prev))
        for i in items[1:]:
            add_edge_enq(self.__id_preg(prev), self.__id_preg(i))
            prev = i
        add_edge_enq(self.__id_preg(prev), "END")

    def visitIdentificador(self, ctx: EnquestesParser.IdentificadorContext):
        """Visit a parse tree produced by EnquestesParser#identificador."""
        return ctx.getText()


del EnquestesParser
