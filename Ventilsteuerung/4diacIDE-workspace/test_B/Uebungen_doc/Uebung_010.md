# Uebung_010: ISOBUS Softkey (Direkt)

[Uebung_010](https://docs.ms-muc-docs.de/projects/visual-programming-languages-docs/de/latest/training1/Ventilsteuerung/4diacIDE-workspace/test/FBs/Uebungen/Uebung_010.html)

[![NotebookLM](media/NotebookLM_logo.png)](https://notebooklm.google.com/notebook/a6872e59-1dfc-4132-a118-aff1bc7bc944)

Dieser Artikel beschreibt die logiBUS®-Übung `Uebung_010`. Hier wird die Anbindung virtueller Bedienelemente eines ISOBUS-Terminals (Universal Terminal, UT) an physische Ausgänge demonstriert.


## Podcast
<iframe src="https://creators.spotify.com/pod/profile/logibus/embed/episodes/LogiBUS--IEC-61499-Daten--und-Ereignisflsse-einfach-erklrt--Vom-Schalter-zur-intelligenten-Steuerung-e36vldb/a-ac3vadb" height="102px" width="400px" frameborder="0" scrolling="no"></iframe>

----



![](Uebung_010.png)


## Ziel der Übung

Verwendung eines `Softkey`-Bausteins zur direkten Steuerung eines digitalen Ausgangs. Es wird gezeigt, wie Ereignis- und Datenverbindungen genutzt werden, um eine Interaktion am Touchscreen in eine physische Aktion umzusetzen.

-----

## Beschreibung und Komponenten

[cite_start]Die Subapplikation `Uebung_010.SUB` verbindet eine Softkey-Instanz mit einem Standard-Ausgangsbaustein[cite: 1].

### Funktionsbausteine (FBs)

  * **`SoftKey_F1`**: Typ `isobus::UT::io::Softkey::Softkey_IX`. Dieser Baustein repräsentiert eine der Tasten am Bildschirmrand oder auf dem Touch-Display des ISOBUS-Terminals.
  * **`DigitalOutput_Q1`**: Der physische Ausgang (z.B. ein Relais oder eine Lampe).

### Parameter

*   **`u16ObjId`**: Diese Kennung verweist auf das entsprechende Objekt im ISOBUS-Pool (hier `SoftKey_F1`).

-----

## Funktionsweise

Die Kommunikation erfolgt über die standardmäßige Trennung von Trigger und Wert:

```xml
<EventConnections>
    <Connection Source="SoftKey_F1.IND" Destination="DigitalOutput_Q1.REQ"/>
</EventConnections>
<DataConnections>
    <Connection Source="SoftKey_F1.IN" Destination="DigitalOutput_Q1.OUT"/>
</DataConnections>
```

[cite_start][cite: 1]

Wenn der Bediener den Softkey am Terminal drückt:
1.  Der Baustein `SoftKey_F1` erkennt die Betätigung über das CAN-Netzwerk.
2.  Er setzt den Datenausgang `IN` auf `TRUE` und feuert ein `IND`-Event.
3.  `DigitalOutput_Q1` empfängt den Trigger und schaltet den Hardware-Ausgang ein.
4.  Beim Loslassen wechselt der Zustand zurück auf `FALSE`, ein erneutes Event wird gesendet und der Ausgang schaltet ab.

-----

## Anwendungsbeispiel

**Hydraulikventil manuell steuern**:
Der Fahrer wählt auf seinem Terminal eine Service-Seite aus. Dort befindet sich ein Button "Ventil spülen". Solange er diesen Button gedrückt hält, wird das entsprechende Magnetventil (`Q1`) angesteuert.
