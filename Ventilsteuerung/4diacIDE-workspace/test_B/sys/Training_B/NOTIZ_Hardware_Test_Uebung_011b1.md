# Notiz: Hardware-Test Uebung_011b1 (feature/Testing_for_Elias)

Dokumentiert den Testaufbau, mit dem `test_B.sys` aktuell (Branch
`feature/Testing_for_Elias`) getestet wird, nachdem `App_B.Control` per
"Change Type" von `Uebung_010a5` auf `Uebung_011b1` umgestellt wurde.

## Testaufbau

- **Übung:** `Uebungen::Uebung_011b1` (`test_B/Uebungen/Uebung_011b1.SUB`)
- **System:** `test_B/sys/Training_B/test_B.sys`, `App_B.Control`
- **VT-Objektpool:** `ISO-DesignerProjects/Workspace/DefaultPool/Output`

## Zielhardware

- **Board:** ESP32-P4, Rev. 0.3
- **Runtime:** 4diac-forte `v0.27-alpha-a-97-gb8dd4796`
- **ESP-IDF:** `v6.0.2d`

## Stand

✅ Erfolgreich getestet auf der echten Hardware: 5+5 = 10.
