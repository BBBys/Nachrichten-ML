from dbparam import DBTDATEN, DBTMELDUNGEN
import mysql.connector
import logging, re, datetime, os

REGEX = r"(?P<Zeit>\d{6});(?P<Mld>.+)"


def DatenSortieren(Datei):
    dir = os.path.dirname(Datei)
    name = os.path.basename(Datei)
    nachDatei = os.path.join(dir, name + ".nach")
    vorDatei = os.path.join(dir, name + ".vor")
    trDat = datetime.datetime.now() + datetime.timedelta(days=-14)
    trenn = trDat.strftime("%y%m%d")

    pattern = re.compile(REGEX)
    logging.info("Daten werden ausgewertet...")
    with open(Datei, "r") as fEin, open(
        nachDatei, "w", encoding="utf-8"
    ) as fNach, open(vorDatei, "w", encoding="utf-8") as fVor:
        zeile = fEin.readline()
        while zeile:
            z = zeile.strip()
            match = pattern.match(z)
            if match:
                zeit = match.group("Zeit")
                mld = match.group("Mld")
                if zeit >= trenn:
                    fNach.write(mld + "\n")
                else:
                    fVor.write(mld + "\n")
            zeile = fEin.readline()

    logging.info("Daten wurden ausgewertet.")

    return (vorDatei, nachDatei)
