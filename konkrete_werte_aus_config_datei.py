from typing import Dict
import yaml
import shutil
import pathlib


def konkrete_werte_aus_config_datei() -> Dict:
    config_pfad = pathlib.Path("config_datei.yaml")
    config = {}
    if config_pfad.is_file():

        with open(config_pfad, "r") as stream:
            config = yaml.safe_load(stream)
    else:
        shutil.copyfile('config_example.yaml', config_pfad)
        raise FileNotFoundError('Die Datei ' + str(config_pfad) + ' mit dem Ordnerpfad ' + str(config_pfad.resolve()) +' hat nicht existiert und wurde nun angelegt. Bitte Werte für spieltag, jahr und kicktipp_ordner_pfad eintragen.')     
    
    return config

def konkreter_wert_jahr_aus_config_datei() -> int:
    config = konkrete_werte_aus_config_datei()
    if type(config['jahr']) is not int:
        raise TypeError("jahr ist nicht vom Datentyp integer. Bitte das Jahr als ganze Zahl eintragen, in dem die Saison beginnt, für die die Auswertung erstellt werden soll.")
    
    else:
        config_jahr = config['jahr']
    return config_jahr

def konkreter_wert_spieltag_aus_config_datei() -> int:
    config = konkrete_werte_aus_config_datei()
    if type(config['spieltag']) is not int:
        raise TypeError("spieltag ist nicht vom Datentyp integer. Bitte den Spieltag für den die Auswertung erstellt werden soll als ganze Zahl eintragen.")
    
    else:
        config_spieltag = config['spieltag']
    return config_spieltag

def konkreter_wert_kicktipp_ordner_pfad_aus_config_datei() -> str:
    config = konkrete_werte_aus_config_datei()
    if type(config['kicktipp_ordner_pfad']) is not str:
        raise TypeError("Der kicktipp_ordner_pfad ist nicht vom Datentyp string. Bitte den Pfad zum Kicktipp Ordner eintragen.")
    
    else:
        config_kicktipp_ordner_pfad = config["kicktipp_ordner_pfad"]
    return config_kicktipp_ordner_pfad