from dbparam import *
import mysql.connector
import logging

DBTCREATEBB = """ CREATE TABLE `blackboard` (
 `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'simpler Zähler',
 `programm` tinytext DEFAULT NULL,
 `version` tinyint(4) DEFAULT 0 COMMENT 'Programmversion, falls es Unterschiede gibt',
 `parameter` tinytext DEFAULT NULL COMMENT 'Parameter für das Programm',
 `parameter2` tinytext DEFAULT NULL COMMENT 'zusätzlicher Parameter',
 `zeit` datetime NOT NULL DEFAULT current_timestamp() COMMENT 'wann der Eintrag erzeugt wurde',
 PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
DBCREATEMELDUNGEN = """CREATE TABLE `meldungen` (
 `hash` bigint(20) NOT NULL COMMENT 'Achtung: ändert sich',
 `datum` timestamp NOT NULL DEFAULT current_timestamp(),
 `quelle` tinytext DEFAULT NULL COMMENT 'Quelle der Meldung',
 `category` tinytext DEFAULT NULL,
 `titel` text DEFAULT NULL,
 `meldung` text DEFAULT NULL,
 `link` tinytext DEFAULT NULL,
 PRIMARY KEY (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
DBCREATEDATEN = """CREATE TABLE `daten` (
 `hash` bigint(20) NOT NULL COMMENT 'Achtung: ändert sich',
 `zeigerRoh` bigint(20) NOT NULL COMMENT 'Hash der Rohmeldung - Vorsicht: nicht konstant',
 `titel` text DEFAULT NULL,
 `meldung` text DEFAULT NULL,
 `w1` tinyint(1) NOT NULL DEFAULT 0 COMMENT 'Einzelwörter erfasst',
 `w2` tinyint(1) NOT NULL DEFAULT 0 COMMENT '2-Wörter erfasst',
 `w3` tinyint(1) NOT NULL DEFAULT 0 COMMENT '3-Wörter erfasst',
 `w4` tinyint(1) NOT NULL DEFAULT 0 COMMENT '4-Wörter erfasst',
 `w5` tinyint(1) NOT NULL DEFAULT 0 COMMENT '5-Wörter erfasst',
 `w10` tinyint(1) NOT NULL DEFAULT 0 COMMENT '10-Wörter erfasst',
 `entr` float DEFAULT 0 COMMENT 'Meldungsentropie',
 `woerter` int(11) DEFAULT NULL,
 `buchstaben` int(11) DEFAULT NULL,
 `kriterium` tinytext DEFAULT NULL COMMENT 'warum diese Meldung als wichtig einestft wurde',
 PRIMARY KEY (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""


def dbcreate(cursor, tabelle):
    """erzeugt eine fehlende Tabelle

    Args:
        cursor (MySQL-Cursor): cursor
        tabelle (string): Tabellenname

    Raises:
        Exception: wenn Name der Tabelle nicht stimmt

    Returns:
        -: 0
    """
    match tabelle:
        case "blackboard":
            cursor.execute(DBTCREATEBB)
        case _:
            raise Exception("Tabelle %s Erzeugung unkekannt" % (tabelle))
    logging.critical("Tabelle nicht vorhanden - erzeugt")
    return 0
