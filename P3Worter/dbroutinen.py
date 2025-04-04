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
DBCREATEMELDUNGEN="""CREATE TABLE `meldungen` (
 `hash` bigint(20) NOT NULL COMMENT 'Vorsicht: nicht fix!',
 `datum` timestamp NOT NULL DEFAULT current_timestamp(),
 `quelle` tinytext DEFAULT NULL COMMENT 'Quelle der Meldung',
 `category` tinytext DEFAULT NULL,
 `titel` text DEFAULT NULL,
 `meldung` text DEFAULT NULL,
 `link` tinytext DEFAULT NULL,
 `status` enum('neu','vereinzelt','kopiert') NOT NULL DEFAULT 'neu',
 PRIMARY KEY (`hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci"""
DBCREATEDATEN="""CREATE TABLE `daten` (
 `hash` bigint(20) NOT NULL COMMENT 'Achtung: ändert sich',
 `zeigerRoh` bigint(20) NOT NULL COMMENT 'Hash der Rohmeldung - Vorsicht: nicht konstant',
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
DBCREATEW1="""CREATE TABLE `woerter1` (
 `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index',
 `wort` tinytext DEFAULT NULL COMMENT 'Wort/Wortfolge',
 `anzahl` int(11) unsigned DEFAULT 1 COMMENT 'absolute Anzahl',
 `gesamt` int(10) unsigned DEFAULT NULL COMMENT 'Gesamtzahl, auf die sich rel. H. bezieht',
 `rang` int(11) unsigned DEFAULT NULL COMMENT 'Rang nach Anzahl',
 `relh` double unsigned DEFAULT NULL COMMENT 'relative Häufigkeit',
 `entr` float unsigned DEFAULT NULL COMMENT 'Wort-Entropie',
 `beitrag` double unsigned DEFAULT NULL COMMENT 'Beitrag zum mittl. Wortentropie (pro Wortkette)',
 `zeichen` tinyint(3) unsigned DEFAULT NULL COMMENT 'Anz. Zeichen in Kette',
 PRIMARY KEY (`id`),
 UNIQUE KEY `wort` (`wort`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='abs. Häufigkeit Wörter'
"""
DBCREATEW2="""CREATE TABLE `woerter2` (
 `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index',
 `wort` tinytext DEFAULT NULL COMMENT 'Wort/Wortfolge',
 `anzahl` int(11) unsigned DEFAULT 1 COMMENT 'absolute Anzahl',
 `gesamt` int(10) unsigned DEFAULT NULL COMMENT 'Gesamtzahl, auf die sich rel. H. bezieht',
 `rang` int(11) unsigned DEFAULT NULL COMMENT 'Rang nach Anzahl',
 `relh` double unsigned DEFAULT NULL COMMENT 'relative Häufigkeit',
 `entr` float unsigned DEFAULT NULL COMMENT 'Wort-Entropie',
 `beitrag` double unsigned DEFAULT NULL COMMENT 'Beitrag zum mittl. Wortentropie (pro Wortkette)',
 `zeichen` tinyint(3) unsigned DEFAULT NULL COMMENT 'Anz. Zeichen in Kette',
 PRIMARY KEY (`id`),
 UNIQUE KEY `wort` (`wort`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='abs. Häufigkeit Wörter'
"""
DBCREATEW3="""CREATE TABLE `woerter3` (
 `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index',
 `wort` tinytext DEFAULT NULL COMMENT 'Wort/Wortfolge',
 `anzahl` int(11) unsigned DEFAULT 1 COMMENT 'absolute Anzahl',
 `gesamt` int(10) unsigned DEFAULT NULL COMMENT 'Gesamtzahl, auf die sich rel. H. bezieht',
 `rang` int(11) unsigned DEFAULT NULL COMMENT 'Rang nach Anzahl',
 `relh` double unsigned DEFAULT NULL COMMENT 'relative Häufigkeit',
 `entr` float unsigned DEFAULT NULL COMMENT 'Wort-Entropie',
 `beitrag` double unsigned DEFAULT NULL COMMENT 'Beitrag zum mittl. Wortentropie (pro Wortkette)',
 `zeichen` tinyint(3) unsigned DEFAULT NULL COMMENT 'Anz. Zeichen in Kette',
 PRIMARY KEY (`id`),
 UNIQUE KEY `wort` (`wort`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='abs. Häufigkeit Wörter'
"""
DBCREATEW4="""CREATE TABLE `woerter4` (
 `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index',
 `wort` tinytext DEFAULT NULL COMMENT 'Wort/Wortfolge',
 `anzahl` int(11) unsigned DEFAULT 1 COMMENT 'absolute Anzahl',
 `gesamt` int(10) unsigned DEFAULT NULL COMMENT 'Gesamtzahl, auf die sich rel. H. bezieht',
 `rang` int(11) unsigned DEFAULT NULL COMMENT 'Rang nach Anzahl',
 `relh` double unsigned DEFAULT NULL COMMENT 'relative Häufigkeit',
 `entr` float unsigned DEFAULT NULL COMMENT 'Wort-Entropie',
 `beitrag` double unsigned DEFAULT NULL COMMENT 'Beitrag zum mittl. Wortentropie (pro Wortkette)',
 `zeichen` tinyint(3) unsigned DEFAULT NULL COMMENT 'Anz. Zeichen in Kette',
 PRIMARY KEY (`id`),
 UNIQUE KEY `wort` (`wort`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='abs. Häufigkeit Wörter'
"""
DBCREATEW5="""CREATE TABLE `woerter5` (
 `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'Index',
 `wort` tinytext DEFAULT NULL COMMENT 'Wort/Wortfolge',
 `anzahl` int(11) unsigned DEFAULT 1 COMMENT 'absolute Anzahl',
 `gesamt` int(10) unsigned DEFAULT NULL COMMENT 'Gesamtzahl, auf die sich rel. H. bezieht',
 `rang` int(11) unsigned DEFAULT NULL COMMENT 'Rang nach Anzahl',
 `relh` double unsigned DEFAULT NULL COMMENT 'relative Häufigkeit',
 `entr` float unsigned DEFAULT NULL COMMENT 'Wort-Entropie',
 `beitrag` double unsigned DEFAULT NULL COMMENT 'Beitrag zum mittl. Wortentropie (pro Wortkette)',
 `zeichen` tinyint(3) unsigned DEFAULT NULL COMMENT 'Anz. Zeichen in Kette',
 PRIMARY KEY (`id`),
 UNIQUE KEY `wort` (`wort`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='abs. Häufigkeit Wörter'
"""

def dbcreate(db,errtext):
    """erzeugt eine fehlende Tabelle

    Args:
        cursor (MySQL-Cursor): cursor
        tabelle (string): Tabellenname

    Raises:
        Exception: wenn Name der Tabelle nicht stimmt

    Returns:
        -: 0
    """
    tabelle=errtext.split("news.")[1].split("'")[0]
    logging.debug(f"dbcreate: {tabelle}")
    with db.cursor() as cursor:
        match tabelle:
            case 'blackboard':cursor.execute(DBTCREATEBB)
            case 'woerter1':cursor.execute(DBCREATEW1)
            case 'woerter2':cursor.execute(DBCREATEW2)
            case 'woerter3':cursor.execute(DBCREATEW3)
            case 'woerter4':cursor.execute(DBCREATEW4)
            case 'woerter5':cursor.execute(DBCREATEW5)
            case _:raise Exception('Tabelle %s Erzeugung unbekannt'%(tabelle))
    logging.critical('Tabelle nicht vorhanden - erzeugt')
    return 0

def zurücksetzenDaten(titel,db,lkette):
    """Daten löschen, zurücksetzen

    Raises:
        Exception: aus falschem Programm
        Exception: nicht zurückgesetzt
    """
    if titel!='P3Worter':
        raise Exception (f"Zurücksetzen aus falschem Programm aufgerufen:{titel}")
    ja=input('Zurücksetzen? Ja:')
    if ja!='Ja':
        raise Exception (f"Zurücksetzen nicht bestätigt: {ja}")
    wMarker=f"w{lkette}"
    wTab=f"woerter{lkette}"
    wAuftr=f"P3{lkette}Worter"
    with db.cursor() as cursor:
        sql=f'truncate {wTab};'
        logging.debug(sql)
        cursor.execute(sql)
        sql=f"insert into {DBTBB} (programm) values ('{wAuftr}');"
        logging.debug(sql)
        cursor.execute(sql)
        sql=f"UPDATE `{DBTDATEN}` SET `{wMarker}`=0;"
        logging.debug(sql)
        cursor.execute(sql)
    db.commit()
    logging.info('...zurückgesetzt')


