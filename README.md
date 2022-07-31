# Kicktipp-Auswertung
Das Programm erstellt die Kicktipp-Auswertung für einen beliebigen Spieltag. Es wird hierbei eine Excel-Datei erstellt.

## Voraussetzungen für die Auswertung
Es muss eine Datei geben, die das Tipper-Kürzel und den dazugehörigen Bundesligisten enthält.
Die Bundesligisten stimmen mit der Schreibweise und Benennung der API (`teamName`) überein:
https://api.openligadb.de/getavailableteams/bl1/2021. Es kann auch die Funktion `mannschaften_aus_api` aus `kürzel_mannschaft.py` aufgerufen werden und es wird eine Liste der Mannschaftsnamen zurückgegeben.
Die Datei muss `Kürzel_Mannschaft.xlsx` heißen, es muss zwei Spalten geben und sie muss im Ordner `Auswertungen_Input/2021` gespeichert werden:

| Kürzel | Mannschaft API |
| -------| ------------ |
| Tipper15 | 1. FSV Mainz 05 |
| Tipper8| TSG 1899 Hoffenheim|
|...|...|

Die Kürzel der Tipper und ihre jeweiligen Kicktipppunkte werden aus Kicktipp als CSV exportiert (`kicktipp-*-Rangliste Einzelwertung_8. Spieltag.csv`) und eingelesen. In der ersten Zeile stehen die Überschriften, die einzelnen Spalten werden durch `;` getrennt.

## Berechnung der Tabelle

Es gibt so viele Tipper wie Bundesligisten in der ersten Bundesliga (18). Jeder Tipper ist einem Bundesligisten zugeordnet. 

Beispiel:

| Tipper | Bundesligist |
| -------| ------------ |
| Tipper15 | 1. FSV Mainz 05 |
| Tipper8| TSG 1899 Hoffenheim|
|...|...|

Jeden Spieltag tippen die zwei Tipper gegeneinander, deren Bundesligisten an diesem Spieltag gegeneinander spielen. 

Am 4. Spieltag hat Mainz gegen Hoffenheim gespielt. Tipper8 hat 18 Kicktipppunkte gesammelt und Tipper15 hat 11 Kicktipppunkte gesammelt. 

| Tipper | Bundesligist |Kicktipppunkte|
| -------| ------------ |-----|
| Tipper15 | 1. FSV Mainz 05 |11|
| Tipper8| TSG 1899 Hoffenheim|18|
|...|...|...|

Die Punkte (die im Folgenden für die Auswertung relevant sind) werden wie folgt vergeben:
Derjenige Tipper, der mehr Kicktipppunkte am jeweiligen Spieltag gesammelt hat, bekommt **3** Punkte. Derjenige Tipper, der weniger Kicktipppunkte gesammelt hat, bekommt **0** Punkte. Haben beide Tipper gleich viele Kicktipppunkte gesammelt, bekommen beide jeweils **1** Punkt.

| Tipper | Bundesligist |Kicktipppunkte|Punkte|
| -------| ------------ |-----|---|
| Tipper15 | 1. FSV Mainz 05 |11|0|
| Tipper8| TSG 1899 Hoffenheim|18|3|
|...|...|...|...|

Die Kicktipppunkte werden als Tore gewertet und daraus wird die Tordifferenz berechnet.

| Tipper | Bundesligist |Kicktipppunkte|Punkte|Tore|Tordifferenz|
| -------| ------------ |-----|---|----|----|
| Tipper15 | 1. FSV Mainz 05 |11|0|11|11-18|
| Tipper8| TSG 1899 Hoffenheim|18|3|18|18-11|
|...|...|...|...|...|...|

Die Tabelle wird anhand der Punkte, Tore, Tordifferenz (Gewichtung in absteigender Reihenfolge) erstellt. Bei Gleichstand von Punkten, Toren und Tordifferenz werden die Platzierungen geteilt.

| Tipper | Bundesligist |Kicktipppunkte|Punkte|Tore|Tordifferenz|Platzierung|
| -------| ------------ |-----|---|----|----|---|
| Tipper8| TSG 1899 Hoffenheim|18|3|18|18-11|1|
| Tipper15 | 1. FSV Mainz 05 |11|0|11|11-18|2|
|...|...|...|...|...|...|...|


Für die Gesamtpunkte/-tore/-tordifferenz werden immer die Punkte/Tore/Tordifferenz der Vorwoche mit den Punkten/Toren/Tordifferenz des aktuellen Spieltags addiert und in der Tabelle ausgegeben.
Zudem wird in der Tabelle sowie die Tendenz im Vergleich zur Vorwochenplatzierung berechnet.

## Erstellung der Auswertungsdatei

Die Excel-Datei enthält drei Tabellenblätter. Das erste enthält die Ergebnisse des aktuellen Spieltages. Die Excel-Datei wird im Ordner `Auswertungen_Output/2021` gespeichert. Die Dateien der vergangenen Spieltage müssen in dem Ordner `Auswertungen_Output/2021` bleiben, da das Programm sich immer den vorherigen Spieltag zur Berechnung der Gesamtpunkte holt.

Beispiel:

| Tipper | Tore|
| -------| -----|
| Tipper15 |11|
| Tipper8|18|
|...|...|

Das zweite Tabellenblatt enthält die Tabelle (s. Berechnung der Tabelle).


Das dritte Tabellenblatt enthält die Begegnungen des nächsten Spieltages.
|Spieltag | Tipper_Heim | Tipper_Gast|
|----|----|----|
|5|Tipper2| Tipper8|
|...|...|...|

# Setup

* Python 3

* venv erstellen: https://docs.python.org/3/library/venv.html --> `python3 -m venv .venv`

* in venv wechseln: `source .venv/bin/activate`
        
  * requirements.txt installieren: `pip install -r requirements.txt`