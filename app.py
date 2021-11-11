# GoDi Plan
# Copyright (C) 2021 KaratekHD.
#
# Dieses Programm ist freie Software. Sie können es unter den Bedingungen der GNU General Public License,
# wie von der Free Software Foundation veröffentlicht, weitergeben und/oder modifizieren, entweder gemäß
# Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren Version.
#
# Die Veröffentlichung dieses Programms erfolgt in der Hoffnung, dass es Ihnen von Nutzen sein wird, aber
# OHNE IRGENDEINE GARANTIE, sogar ohne die implizite Garantie der MARKTREIFE oder der VERWENDBARKEIT FÜR
# EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License.
#
# Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben. Falls
# nicht, siehe <https://www.gnu.org/licenses/>.
#

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import configparser

import requests
from flask import Flask, render_template
from ics import Calendar


# @dataclass sorgt dafür, dass wir kein 'def __init__()' benötigen
@dataclass
class GoDi:
    '''
    Datenklasse für Gottesdienste.
    Jeder Eigenschaft ist ein Attribut.
    Title, Ersteller und Zeit sind definitiv notwendig, alles andere ist optional,
    da die Daten lediglich aus der Beschreibung gezogen werden.
    '''
    title: str
    time: datetime
    predigt: Optional[str]
    lesung: Optional[str]
    dienst: Optional[str]
    orgel: Optional[str]
    kollekte: Optional[str]
    ressourcen: Optional[List[str]]
    creator: str

    def dict(self) -> dict:
        '''
        Erstellt ein dict aus den Eigenschaften dieser Klasse.
        Wird derzeit für nichts benötigt, könnte aber später sinnvoll sein.
        Macht es außerdem leichter, beim Debuggen die Daten auszugeben.
        '''
        return {
            'title': self.title,
            'time': self.time.isoformat(),
            'predigt': self.predigt,
            'lesung': self.lesung,
            'dienst': self.dienst,
            'orgel': self.orgel,
            'kollekte': self.kollekte,
            'ressourcen': self.ressourcen,
            'creator': self.creator
        }

    def date(self):
        return self.time.strftime('%d.%m')

    def time_str(self):
        return self.time.strftime('%H:%M')

    def fancy_resources(self):
        if self.ressourcen:
            return ', '.join(self.ressourcen)
        else:
            return ''


def parse(url: str) -> str:
    # Herunterladen der Kalender-Datei und laden in ein Objekt
    c = Calendar(requests.get(url).text)
    # In dieser Liste werden alle Gottesdienste gespeichert
    events = []  # Type: List[GoDi]
    for e in c.events:
        # So that we have an empty string instead of None
        predigt, lesung, dienst, orgel, kollekte, ressourcen, creator = "", "", "", "", "", "", ""

        # Laden der relevanten Informationen aus dem Event
        date = datetime.strptime(str(e.begin), "%Y-%m-%dT%H:%M:%S%z")
        # Die Beschreibung in Mundgerechte Stücke zerlegen
        data = e.description.split("\n")
        for i in data:
            # Alles hier drinnen steht in der Beschreibung
            if i.startswith("Predigt: "):
                predigt = i.replace("Predigt: ", "")
            if i.startswith("Lesung:"):
                lesung = i.replace("Lesung: ", "")
            if i.startswith("Dienst: "):
                dienst = i.replace("Dienst: ", "")
            if i.startswith("Organist: "):
                orgel = i.replace("Organist: ", "")
            if i.startswith("Kollekte: "):
                kollekte = i.replace("Kollekte: ", "")
            if i.startswith("Ressourcen: "):
                ressourcen = i.replace("Ressourcen: ", "").split(", ")
            if i.startswith("Erstellt von: "):
                creator = i.replace("Erstellt von: ", "")
        # Erstellen eines Objekts aus den Informationen
        godi = GoDi(
            title=e.name,
            time=date,
            predigt=predigt,
            lesung=lesung,
            dienst=dienst,
            orgel=orgel,
            kollekte=kollekte,
            ressourcen=ressourcen,
            creator=creator)
        # Speichern des Objekts in der Liste
        events.append(godi)
    # Sortieren der Liste nach Datum
    events.sort(key=lambda x: x.time)
    return events

# Laden der Werte aus der Konfigurationsdatei
config = configparser.ConfigParser()
config.read('config.ini')
navbar = config["default"].getboolean("navbar")
footer = config["default"].getboolean("footer")
devmode = config["development"].getboolean("devmode")
title = config["default"]['title']
logo = config["default"]['logo']
url = config["default"]['url']
name = config["default"]['name']



# Initialisierung des Servers
app = Flask(__name__)


@app.route("/")
def table():
    # In der Vorlage steht all das HTML, und wir füllen es hier mit Inhalten
    return render_template("template.html", show_navbar=navbar, events=parse(url), title=title, logo=logo, show_footer=footer, devmode=devmode, name=name)


# Wird nur ausgeführt, wenn die Datei direkt aufgerufen wird
if __name__ == "__main__":
    # App ausführen
    app.run(debug=devmode)