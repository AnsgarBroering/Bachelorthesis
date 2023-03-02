## Themen  

### Thema 1 - Vergleich - PyPSA und pandapower
- Vergleich von Energie-Frameworks 
- Übersicht welche Frameworks gibt es in der Energieinformatik-Forschung
	- ggf. auch Schnittstelle zu Stephan Ferenz
	- Aufbereiten, welche Features haben die Frameworks
- Kleines Requirements Engineering in der Abteilung DES
	- "Wozu benutzt ihr die Frameworks, was sind eure Anfroderungen?"
	- Art Anforderungskatalog mit Anforderungen erstellen
- Dann Frameworks hinsichtlich der Anforderungen untersuchen
- Anschließend prototypisch einzelne Szenarien umsetzen (in beiden/allen Frameworks), um Anforderungen zu evaluieren

### Thema 2 - Lernen der Value Function einer Coalition mit ANN
- ANN = Artificial Neural Net
- CF = Coalition Formation
- Einfaches CF Beispiel 
	- Agenten bilden Koalitionen um ihren Wert zu maximieren
	- Jeder Agent hat z.B. eine Ressource/Farbe/whatever 
	- Wenn Agenten kooperieren (eine Koalition bilden) ist ihr Payoff größer
	- Wie entscheidet man, welcher Agent einer Koalition beitreten darf oder nicht?
		- Man lernt die Value Function anhand derer ein Agent (z.B. Coalition Initiator) den Wert mit und ohne einen Agenten bestimmen kann und entscheidet anhand der Funktion, ob der Agent der Koalition beitreten darf oder nicht 
- Idee: Lernen der value function zur Coalition Formation mittels eines ANNs
	- Zuvor Daten erzeugen anhand einer eigenen Funktion
- Offen: Kann man dafür ein simples Energie-Szenario finden? 

## Orga
- Anmelden im Februar
- Mit oder ohne Forschungsseminar?