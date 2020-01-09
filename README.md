# QuizBot

Projecte QuizBot per GEI-LP (edició tardor 2019)

### Detalls de d'implementació:

- Totes les comandes s'executen des del directori arrel de la pràctica.
- Un fitxer d'enquesta pot tenir més d'una enquesta, però els IDs de cada
pregunta són únics i no depenen de l'enquesta. Això vol dir que una enquesta
pot utilitzar preguntes d'altres enquestes.

### Prerequisits

Per instal·lar les llibreries no estàndards usades en el projecte:

```bash
$ pip3 install -r requirements.txt
```

### Execució

El projecte consta de dos programes, el compilador que parseja els fitxer d'enquesta i genera
objectes de networkx i el bot que llegeix aquests objectes i interactua amb els usuaris.

#### Compilador

Per executar el compilador de la gramàtica i generar el gràfic i el pickle amb el graf de
networkx executarem:

```bash
$ python3 cl/test.py <enquesta.txt> <nom_fitxer_sortida>
```

El següent exemple parseja l'enquesta d'exemple que es troba en el fitxer `test/text.txt` i
genera una gràfica a `graf.png` i un pickle amb el graf de networkx a `graf.pckl`:
```bash
$ python3 cl/test.py test/text.txt graf
```

#### Telegram bot

Per executar el bot, passarem com a paràmetre l'arxiu pickle generat amb el
compilador que conté el graf de networkx de l'enquesta.

```bash
$ python3 bot/bot.py <fitxer.pckl>
```

Seguint l'exemple de l'apartat anterior (`graf.pckl`):

```bash
$ python3 bot/bot.py graf.pckl
```

URL del bot: t.me/***REMOVED*** 

## Built With

* [ANTLR4](https://www.antlr.org/) - ANother Tool for Language Recognition
* [matplotlib](https://matplotlib.org/) - Generar gràfiques
* [networkx](https://networkx.github.io/) - Manipulació de grafs
* [python-telegram-bot](https://python-telegram-bot.org/) - Embolcall de l'API de bot de telegram per python

## Authors

* *****REMOVED***** - [***REMOVED***](mailto:***REMOVED***)

