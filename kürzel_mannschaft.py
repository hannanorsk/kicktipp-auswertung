from typing import List
import urllib.request 
import json
import pandas as pd
import konkrete_werte_aus_config_datei

# Diese Datei wird am Saisonstart benötigt, um einmal alle diesjährigen Mannschaften der Bundesliga in der API-Schreibweise zu erhalten. 

config_jahr = konkrete_werte_aus_config_datei.konkreter_wert_jahr_aus_config_datei()

def mannschaften_aus_api(jahr) -> List[str]:
    '''
    Die Funktion gibt die Mannschaftsnamen der API/Schnittstelle zurück.    
    '''
    
    response = urllib.request.urlopen('https://api.openligadb.de/getavailableteams/bl1/'+str(jahr)).read().decode()
    
    mannschaften = json.loads(response)
    liste = []
    for teams in mannschaften:
        mannschaftsname = (teams['teamName'])
        liste.append(mannschaftsname)
    
    return liste  

uebersicht_mannschaften = pd.DataFrame({'Mannschaften': mannschaften_aus_api(config_jahr)})
print(uebersicht_mannschaften)
