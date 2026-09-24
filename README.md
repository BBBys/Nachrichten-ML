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
* liest Datei mit vom Feed abgerufenen Meldungen
  * Meldungen bestehen aus
  * Titel
  * Inhalt
  * weiteren Angaben
* Meldungen werden nur so weit aufbereitet, dass sie in der DB gespeichert werden können
  * z.B.kein >'<
  * Stopp-Wörter werden erst im nächsten Schritt behandelt
* schreibt Meldungen in Datenbank

## 3. P21Stop 

* löscht doppelte Meldungen
* Titel und Meldung zusammenfassen
* Sonderzeichen und Stoppwörter entfernen,
* in Kleinschreibung umwandeln, 
* in Tabelle daten speichern

Dabei werden ein paar Umwandlungen gemacht, z.B.

aus|wird
---|---
&amp;| und 
d.h.|das heisst
z.b.|zum beispiel
ß|ss
    
## 4. Types und Anzahl erfassen

### P3-Programme

Jedes Programm 
* holt die um Stoppwörter bereinigten Meldungen aus der Datenbank und 
* zerlegt sie in Token 
  * Einzelwörter oder n-Wortfolgen, gesteuert durch Parameter
* Zählt die Types 
* schreibt die Summen für jeden Type in die passende Tabelle

## 6. P6altneu
* vergleicht die Häufigkeit von Wörtern in allen Aufzeichnungen mit der in den letzten x Tagen (x z,B. 7)
* listet auf, was signifikant häufiger ist
## NMLlib

... fasst zentrale Module zusammen
Einbinden mit ```export PYTHONPATH="../NMLlib"```

# To Do
[ ] ML-Verfahren für P6altneu einsetzen

# Lizenz

Nachrichten-ML  © 2025-2026 by Dr. Burkhard Borys 
is licensed under CC BY-NC-ND 4.0. 
To view a copy of this license, visit 
https://creativecommons.org/licenses/by-nc-nd/4.0/

# Quellen

    [1] Mit Hilfe von VS Code's Copilot.

    [2]. Alberto Boschetti and Luca Massaron, Python data science essentials : become an 
    efficient data science practitioner by understanding Python’s key concepts. Packt 
    Publishing, 2016.
  