# GoDi Plan
Diese Flask Anwendung kann verwendet werden, um Gottesdienstpläne aus Intern-E in Tabellen anzuzeigen.

## Schnellstart
Als erstes sollten die Abhängigkeiten installiert werden:
```bash
pip install -r requirements.txt
```
Anschließend muss `config.ini` mit Inhalten gefüllt werden:

| Key   | Inhalt        | Typ   |
| ----- | ------------- | ----- |
| navbar | Legt fest, ob die Kopfzeile angezeigt werden soll | Boolean |
| footer | Legt fest, ob die Fußzeile angezeigt werden soll | Boolean |
| title  | Titel der Seite | String |
| logo   | URL zum (externen) Logo | String |
| url    | URL zur .ical Datei | String |
| devmode | Sollte im Deployment auf False gesetzt werden | Boolean |

Hierfür kann die Datei `config-sample.ini` verwendet werden.

Nun kann der Server mittels `python3 app.py` gestartet werden.

## Aufbau der Kalendereinträge
Abgesehen von den Standardinformationen aus der .ics Datei, werden folgende Daten aus der Beschreibung gelesen, sollten Sie angegeben sein:

- Prediger
- Organist
- Lektor
- Dienst
- Kollekte 
- Resourcen (aus Intern-E)

Die Daten sollten jeweils in einer neuen Zeile in die Beschreibung eingefügt werden:
```
Predigt: [Name]
Organist: [Name]
[...]
```

## Credits
Diese Anwendung verwendet das openSUSE Design System: <https://static.opensuse.org/chameleon>

## Lizenz
Dieses Programm ist freie Software. Sie können es unter den Bedingungen der GNU General Public License,
wie von der Free Software Foundation veröffentlicht, weitergeben und/oder modifizieren, entweder gemäß
Version 3 der Lizenz oder (nach Ihrer Wahl) jeder späteren Version.

Die Veröffentlichung dieses Programms erfolgt in der Hoffnung, dass es Ihnen von Nutzen sein wird, aber
OHNE IRGENDEINE GARANTIE, sogar ohne die implizite Garantie der MARKTREIFE oder der VERWENDBARKEIT FÜR
EINEN BESTIMMTEN ZWECK. Details finden Sie in der GNU General Public License.

Sie sollten ein Exemplar der GNU General Public License zusammen mit diesem Programm erhalten haben. Falls
nicht, siehe <https://www.gnu.org/licenses/>.	