from auswertung import path_auswertungsdatei
import auswertung
import hilfsfunktionen
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import konkrete_werte_aus_config_datei
import numpy as np
import matplotlib

config_spieltag = konkrete_werte_aus_config_datei.konkreter_wert_spieltag_aus_config_datei()

alle_spieltage = range(1,config_spieltag+1,1)
Rang_Platzierung_Spieltag = []
for spieltag in alle_spieltage:
    xlsx_path = auswertung.path_auswertungsdatei(konkrete_werte_aus_config_datei.konkreter_wert_kicktipp_ordner_pfad_aus_config_datei(), konkrete_werte_aus_config_datei.konkreter_wert_jahr_aus_config_datei(), spieltag)
    df_Rang_Coach = hilfsfunktionen.excel_to_dataframe(xlsx_path, 'Tabelle')
    Rang_Platzierung =df_Rang_Coach[['Rang','Coach']]
    Rang_Platzierung['Spieltag']= spieltag
    erweiterung = list(Rang_Platzierung.itertuples(index=False, name=None))
    Rang_Platzierung_Spieltag.extend(erweiterung)

Gesamtdaten = pd.DataFrame(Rang_Platzierung_Spieltag, columns=['Rang', 'Coach', 'Spieltag'])

xlsx_path = auswertung.path_auswertungsdatei(konkrete_werte_aus_config_datei.konkreter_wert_kicktipp_ordner_pfad_aus_config_datei(), konkrete_werte_aus_config_datei.konkreter_wert_jahr_aus_config_datei(), config_spieltag)
df_Rang_Coach = hilfsfunktionen.excel_to_dataframe(xlsx_path, 'Tabelle')


number_of_coaches = df_Rang_Coach['Coach'].count()
plt.rcParams["figure.figsize"] = 16, 8
sns.lineplot(data= Gesamtdaten, x="Spieltag", y="Rang", hue='Coach', hue_order=df_Rang_Coach['Coach'], palette=sns.color_palette("tab20")[0:number_of_coaches], marker="o")
plt.xticks(np.arange(1,config_spieltag+1, step=1))

plt.yticks(np.arange(1,number_of_coaches+1, step=1))
plt.gca().invert_yaxis()
plt.grid(axis='y')
plt.legend(bbox_to_anchor=(1.04,0.97), borderaxespad=0, labelspacing=1.375)

plt.savefig("Verlaufsgrafik.svg", bbox_inches="tight")
