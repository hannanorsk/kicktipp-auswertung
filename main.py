from asyncio import constants
from os import path
from typing import Dict
import auswertung
from datei_ordner_pfade import ausgabe_ordner_anlegen, eingabe_ordner_anlegen
import konkrete_werte_aus_config_datei
import constants


config_spieltag = konkrete_werte_aus_config_datei.konkreter_wert_spieltag_aus_config_datei()
config_jahr = konkrete_werte_aus_config_datei.konkreter_wert_jahr_aus_config_datei()
config_kicktipp_ordner_pfad = konkrete_werte_aus_config_datei.konkreter_wert_kicktipp_ordner_pfad_aus_config_datei()

eingabe_ordner_anlegen(config_kicktipp_ordner_pfad, constants.eingabe_pfad, config_jahr)
ausgabe_ordner_anlegen(config_kicktipp_ordner_pfad, constants.unterordner_output, config_jahr)

liste = range(1,config_spieltag+1)
#liste = [config_spieltag]
for spieltag in liste:
    

    print("erstelle Auswertung für Spieltag " + str(spieltag))

    if spieltag == 1:
        excel_pfad_auswertungsdatei = auswertung.erstelle_auswertungsdatei_spieltag_1(config_jahr, config_kicktipp_ordner_pfad)
        
    else:
        excel_pfad_auswertungsdatei = auswertung.erstelle_auswertungsdatei_ab_spieltag_2(
            spieltag,
            jahr = config_jahr,
            xlsx_path_vorwoche = auswertung.path_auswertungsdatei(config_kicktipp_ordner_pfad, config_jahr, spieltag -1),
            kicktipp_pfad = config_kicktipp_ordner_pfad
        )

    print("Auswertung für Spieltag " + str(spieltag) + " wurde in " + excel_pfad_auswertungsdatei + " erstellt.")
