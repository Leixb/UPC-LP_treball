grammar Enquestes;

root : enquesta+ EOF ;

enquesta : ( preg | resp | item | alte | enqu )+ END NL? ;

preg : identificador SEP PREGUNTA NL text_pregunta NL ;
text_pregunta : ( INT | WORD | ID | SEMI | COMMA | LPAR | RPAR | LCLAU | RCLAU | ARROW | PREGUNTA | RESPOSTA | ITEM | ALTERNATIVA | ENQUESTA )+ ;

resp : identificador SEP RESPOSTA NL opcions_resposta ;
opcions_resposta : opcio_resposta+ ;
opcio_resposta : id_opcio SEP text_opcio ;
text_opcio : (INT | WORD | ID | COMMA | LPAR | RPAR | LCLAU | RCLAU | ARROW | PREGUNTA | RESPOSTA | ITEM | ALTERNATIVA | ENQUESTA )+ (SEMI | NL) NL? ;
id_opcio : INT ;

item : identificador SEP ITEM NL id_preg ARROW id_resp NL ;
id_preg : ID ;
id_resp : ID ;

alte : identificador SEP ALTERNATIVA NL id_preg alternatives NL ;
alternatives : LCLAU alternativa+ RCLAU ;
alternativa : LPAR id_opcio COMMA id_preg RPAR COMMA? ;

enqu : identificador SEP ENQUESTA NL id_preg+ NL ;

identificador : ID ;


INT : [0-9]+ ;

WS : [\t ]+ -> skip ;

NL : '\n' ;

SEP : ':' WS ;
COMMENT         : WS '//' ~[\r\n]* -> skip ;

END : 'END' ;

PREGUNTA    : 'PREGUNTA' ;
RESPOSTA    : 'RESPOSTA' ;
ITEM        : 'ITEM' ;
ALTERNATIVA : 'ALTERNATIVA' ;
ENQUESTA    : 'ENQUESTA' ;

ID : [a-zA-Z][a-zA-Z0-9\u0080-\u00FF]* ;

SEMI : ';' ;

ARROW : '->' ;

COMMA : ',' ;
LPAR : '(' ;
RPAR : ')' ;
LCLAU : '[' ;
RCLAU : ']' ;

WORD : ~[ ()[\],\t\n\r:]+ ;
