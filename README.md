[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Nachrichten - Python - Machine Learning

RSS-Feeds mit ML-Verfahren bearbeiten. In dieser Version alles in Python
![image](151214.jpeg)

## Quellen der Nachrichten
* :newspaper: SPIEGEL
* :tv: Tagesschau

## Abfrage
im Abstand von min. 5 Stunden und Speicherung von Titel, Kurzfassung, Link zur Vollmeldung

### Wort- und Wortfolgen-Häufigkeiten
* 1-, 3- und 5-Wort-Ketten
* nach Ausblenden von :stop_sign: Stopp-Wörtern
* für gesamten Beobachtungszeitraum und die letzte Woche

# Der Ablauf

## 0. P0Abrufen
* liest Auftrag *P0Arufen* von Blackboard
  * ergibt Record mit SPIEGEL oder TAGESSCHAU und Datum/Uhrzeit
  * wenn nicht: diese 2 Records werden erzeugt, Exit
* wieviel Zeit ist vergangen?
  * zu wenig: Exit
  * das ist wichtig, um die RSS-Server nicht unnötig zu beanspruchen und in den Verdacht eies DoS-Angriffs zu kommen
* liest RSS ein
* schreibt ohne Veränderung in Datei
* schreibt Auftrag für *P2Eintragen* und Dateinamen in Blackboard
* schreibt neuen Auftrag für *P0Abrufen* und Zeit in Blackboard
* löscht bearbeiteten Record aus Blackboard
## 1.
ist irgendwo verloren :dizzy_face: gegangen
## 2. P2Eintragen
* liest von Blackboard
  * ergibt Record mit Dateinamen

## 6. P6altneu
* vergleicht die Häufigkeit von Wörtern in allen Aufzeichnungen mit der in den letzten x Tagen (x z,B. 7)
* listet auf, was signifikant häufiger ist

# To Do
[ ] ML-Verfahren für P6altneu einsetzen
