#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  DBCreate.py
#
#
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
