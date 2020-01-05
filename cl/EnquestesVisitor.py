# Generated from Enquestes.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EnquestesParser import EnquestesParser
else:
    from EnquestesParser import EnquestesParser

# This class defines a complete generic visitor for a parse tree produced by EnquestesParser.

class EnquestesVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by EnquestesParser#root.
    def visitRoot(self, ctx:EnquestesParser.RootContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        return [self.visit(i) for i in l[:-1]]


    # Visit a parse tree produced by EnquestesParser#enquesta.
    def visitEnquesta(self, ctx:EnquestesParser.EnquestaContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        return [self.visit(i) for i in l[:-2]]


    # Visit a parse tree produced by EnquestesParser#preg.
    def visitPreg(self, ctx:EnquestesParser.PregContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        pregunta = dict()
        pregunta["id"] = self.visit(l[0])
        pregunta["text"] = self.visit(l[4])
        return pregunta


    # Visit a parse tree produced by EnquestesParser#text_pregunta.
    def visitText_pregunta(self, ctx:EnquestesParser.Text_preguntaContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [str(next(g)) for i in range(n_children)]
        return ' '.join(l)


    # Visit a parse tree produced by EnquestesParser#resp.
    def visitResp(self, ctx:EnquestesParser.RespContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        resposta = dict()
        resposta["id"] = self.visit(l[0])
        resposta["opcions"] = self.visit(l[4])
        return resposta


    # Visit a parse tree produced by EnquestesParser#opcions_resposta.
    def visitOpcions_resposta(self, ctx:EnquestesParser.Opcions_respostaContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [self.visit(next(g)) for i in range(n_children)]
        return l


    # Visit a parse tree produced by EnquestesParser#opcio_resposta.
    def visitOpcio_resposta(self, ctx:EnquestesParser.Opcio_respostaContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        opcio = dict()
        opcio["id"] = self.visit(l[0])
        opcio["text"] = self.visit(l[2])
        return opcio
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EnquestesParser#text_opcio.
    def visitText_opcio(self, ctx:EnquestesParser.Text_opcioContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [str(next(g)) for i in range(n_children)]
        text = ' '.join(l)
        return text.split(';')[0].strip()


    # Visit a parse tree produced by EnquestesParser#id_opcio.
    def visitId_opcio(self, ctx:EnquestesParser.Id_opcioContext):
        g = ctx.getChildren()
        return int(next(g).getText())
        return self.visitChildren(ctx)


    # Visit a parse tree produced by EnquestesParser#item.
    def visitItem(self, ctx:EnquestesParser.ItemContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        item = dict()
        item["id"] = self.visit(l[0])
        item["id_preg"] = self.visit(l[4])
        item["id_resp"] = self.visit(l[6])
        return item


    # Visit a parse tree produced by EnquestesParser#id_preg.
    def visitId_preg(self, ctx:EnquestesParser.Id_pregContext):
        return ctx.getText()


    # Visit a parse tree produced by EnquestesParser#id_resp.
    def visitId_resp(self, ctx:EnquestesParser.Id_respContext):
        return ctx.getText()


    # Visit a parse tree produced by EnquestesParser#alte.
    def visitAlte(self, ctx:EnquestesParser.AlteContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        alternativa = dict()
        alternativa["id"] = self.visit(l[0])
        alternativa["id_preg"] = self.visit(l[4])
        alternativa["alternatives"] = self.visit(l[5])
        return alternativa


    # Visit a parse tree produced by EnquestesParser#alternatives.
    def visitAlternatives(self, ctx:EnquestesParser.AlternativesContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        l = l[1:-1]
        return [self.visit(i) for i in l]


    # Visit a parse tree produced by EnquestesParser#alternativa.
    def visitAlternativa(self, ctx:EnquestesParser.AlternativaContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        alternativa = dict()
        alternativa["id_opcio"] = self.visit(l[1])
        alternativa["id_item"] = self.visit(l[3])
        return alternativa


    # Visit a parse tree produced by EnquestesParser#enqu.
    def visitEnqu(self, ctx:EnquestesParser.EnquContext):
        n_children =  ctx.getChildCount()
        g = ctx.getChildren()
        l = [next(g) for i in range(n_children)]
        enquesta = dict()
        enquesta['id'] = self.visit(l[0])
        enquesta['items'] = [self.visit(i) for i in l[4:-1]]
        return enquesta


    # Visit a parse tree produced by EnquestesParser#identificador.
    def visitIdentificador(self, ctx:EnquestesParser.IdentificadorContext):
        return ctx.getText()



del EnquestesParser
