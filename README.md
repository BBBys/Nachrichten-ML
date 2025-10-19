[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Nachrichten - Python - Machine Learning
 RSS-Feeds mit ML-Verfahren bearbeiten. In dieser Version alles in Python
![image](151214.jpeg)
## Quellen
* SPIEGEL
* Tagesschau
## Abfrage
im Abstand von min. 5 Stunden und Speicherung von Titel, Kurzfassung, Link zur Vollmeldung
### Wort- und Wortfolgen-Häufigkeiten
* 1-, 3- und 5-Wort-Ketten
* nach Ausblenden von Stopp-Wörtern
* für gesamten Beobachtungszeitraum und die letzte Woche
### Wort- und Wortfolgen-Häufigkeiten
* 1-, 3- und 5-Wort-Ketten
* nach Ausblenden von Stopp-Wörtern
* für gesamten Beobachtungszeitraum und die letzte Woche
# Ablauf
## 1. P0Abrufen
* liest P0Arufen von Blackboard
  * ergibt Record mit SPIEGEL oder TAGESSCHAU und Datum/Uhrzeit
  * wenn nicht: 2 Records weren erzeugt, Exit
* wieviel Zeit ist vergangen?
  * zu wenig: Exit
* liest RSS ein
* schreibt ohne Veränderung in Datei
* schreibt P2Eintragen und Dateinamen in Blackboard
* schreibt P0Abrufen und Zeit in Blackboard
* löscht bearbeiteten Record aus Blackboard

## 2. P2Eintragen
* liest von Blackboard
  * ergibt Record mit Dateinamen
* 

