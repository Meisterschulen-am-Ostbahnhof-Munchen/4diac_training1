"""Erzeugt Uebung_269..272_AX (Dialog-Lib) in training1/test_AX/Uebungen.

Aufruf: python gen_dialog_uebungen.py <training1_root>
"""
import sys
from pathlib import Path
from xml.sax.saxutils import escape

out = Path(sys.argv[1]) / 'Ventilsteuerung' / '4diacIDE-workspace' / 'test_AX' / 'Uebungen'
POOL = 'Uebungen::const::UT::Dialog::DefaultPool'
DLGC = 'isobus::UT::dialog::DialogConst'
COPY = ('Copyright (c) 2026 Meisterschulen am Ostbahnhof  &#10; &#10;This program and the accompanying materials are made  &#10;'
        'available under the terms of the Eclipse Public License 2.0  &#10;which is available at https://www.eclipse.org/legal/epl-2.0/  &#10; &#10;'
        'SPDX-License-Identifier: EPL-2.0')


class Ex:
    def __init__(self):
        self.fbs, self.ev, self.data, self.imp = [], [], [], set()

    def fb(self, name, typ, x, y, params=()):
        p = ''.join(f'\t\t\t<Parameter Name="{k}" Value="{escape(v)}"/>\n' for k, v in params)
        self.fbs.append(f'\t\t<FB Name="{name}" Type="{typ}" x="{x}" y="{y}">\n{p}\t\t</FB>\n')

    def pool(self, c):
        self.imp.add(f'{POOL}::{c}')
        return c

    def const(self, c):
        self.imp.add(f'{DLGC}::{c}')
        return c

    def e(self, s, d):
        self.ev.append(f'\t\t\t<Connection Source="{s}" Destination="{d}"/>\n')

    def d(self, s, d):
        self.data.append(f'\t\t\t<Connection Source="{s}" Destination="{d}"/>\n')

    def write(self, name, comment):
        imp = ''.join(f'\t\t<Import declaration="{i}"/>\n' for i in sorted(self.imp))
        txt = f'''<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="{name}" Comment="{escape(comment)}">
	<Identification Standard="61499-2" Description="{COPY}">
	</Identification>
	<VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1.0" Author="Franz Höpfinger" Date="2026-11-17" Remarks="initial API and implementation and/or initial documentation">
	</VersionInfo>
	<CompilerInfo packageName="Uebungen">
{imp}	</CompilerInfo>
	<SubAppInterfaceList>
	</SubAppInterfaceList>
	<SubAppNetwork>
{''.join(self.fbs)}		<EventConnections>
{''.join(self.ev)}		</EventConnections>
		<DataConnections>
{''.join(self.data)}		</DataConnections>
	</SubAppNetwork>
</SubAppType>
'''
        (out / f'{name}.SUB').write_text(txt, encoding='utf-8', newline='\n')


def softkey(x, name, sk, y):
    x.imp.add('isobus::UT::io::Softkey::SoftKeyActivationCode::SK_RELEASED')
    x.fb(name, 'isobus::UT::io::Softkey::Softkey_IE', -6000, y,
         [('QI', 'TRUE'), ('u16ObjId', x.pool(sk)), ('InputEvent', 'SK_RELEASED')])


def init_fb(x, target):
    x.fb('INIT', 'events::init::INIT', -6000, -2500)
    x.e('INIT.INITO', f'{target}.INIT')


def result_display(x, src):
    x.fb('RESULT_TO_UDINT', 'iec61131::conversion::F_USINT_TO_UDINT', 1500, 0)
    x.fb('Q_Result', 'isobus::UT::Q::Q_NumericValue', 3500, 0, [('QI', 'TRUE'), ('u16ObjId', x.pool('OutputNumber_Result'))])
    x.e(f'{src}.CNF', 'RESULT_TO_UDINT.REQ')
    x.d(f'{src}.RESULT', 'RESULT_TO_UDINT.IN')
    x.e('RESULT_TO_UDINT.CNF', 'Q_Result.REQ')
    x.d('RESULT_TO_UDINT.OUT', 'Q_Result.u32NewValue')


def test_buttons(x):
    x.imp.add('isobus::UT::io::Button::ButtonActivationCode::BT_RELEASED_UNLATCHED')
    for n, val in ((1, 101), (2, 102)):
        x.fb(f'Button_Test{n}', 'isobus::UT::io::Button::Button_IE', -6000, 2000 + n * 1200,
             [('QI', 'TRUE'), ('u16ObjId', x.pool(f'Button_Test{n}')), ('InputEvent', 'BT_RELEASED_UNLATCHED')])
        x.fb(f'Q_Test{n}', 'isobus::UT::Q::Q_NumericValue', -2500, 2000 + n * 1200,
             [('QI', 'TRUE'), ('u16ObjId', 'OutputNumber_Result'), ('u32NewValue', f'UDINT#{val}')])
        x.e(f'Button_Test{n}.IND', f'Q_Test{n}.REQ')


# 269 Toast
x = Ex()
init_fb(x, 'Toast')
softkey(x, 'SoftKey_Toast', 'SoftKey_F1', -1000)
x.fb('Toast', 'isobus::UT::dialog::DLG_Toast', -2500, -1000,
     [('TEXT_ID', x.pool('OutputString_Text_Toast')), ('ICON', x.const('DLG_ICON_INFO')), ('TIMEOUT', 'T#3s')])
x.e('SoftKey_Toast.IND', 'Toast.SHOW')
x.write('Uebung_269_AX', 'Dialog: Toast (Hinweis ohne Tasten, verschwindet nach 3 s), Pool Dialog')

# 270 / 271 MessageBox OK nicht modal / modal
for nr, modal, sk in ((270, 'FALSE', 'SoftKey_F2'), (271, 'TRUE', 'SoftKey_F3')):
    x = Ex()
    init_fb(x, 'MsgBox')
    softkey(x, 'SoftKey_Show', sk, -1000)
    x.fb('MsgBox', 'isobus::UT::dialog::DLG_MessageBox', -2500, -1000,
         [('TEXT_ID', x.pool('OutputString_Text_OK')), ('ICON', x.const('DLG_ICON_WARNING')),
          ('BUTTONS', x.const('DLG_BTN_OK')), ('MODAL', modal)])
    x.e('SoftKey_Show.IND', 'MsgBox.SHOW')
    result_display(x, 'MsgBox')
    test_buttons(x)
    art = 'modal: Test-Buttons gesperrt' if modal == 'TRUE' else 'nicht modal: Test-Buttons bedienbar'
    x.write(f'Uebung_{nr}_AX', f'Dialog: MessageBox OK, {art}, RESULT im Zahlenfeld')

# 272 Ja/Nein/Abbrechen, Default Nein, Timeout, Ton
x = Ex()
init_fb(x, 'MsgBox')
softkey(x, 'SoftKey_Show', 'SoftKey_F4', -1000)
x.fb('MsgBox', 'isobus::UT::dialog::DLG_MessageBox', -2500, -1000,
     [('TEXT_ID', x.pool('OutputString_Text_Frage')), ('ICON', x.const('DLG_ICON_QUESTION')),
      ('BUTTONS', x.const('DLG_BTN_YESNOCANCEL')), ('DEFAULT_BUTTON', 'USINT#2'), ('MODAL', 'TRUE'),
      ('TIMEOUT', 'T#10s'), ('AUDIO', 'TRUE')])
x.e('SoftKey_Show.IND', 'MsgBox.SHOW')
result_display(x, 'MsgBox')
x.write('Uebung_272_AX', 'Dialog: Ja/Nein/Abbrechen, Fokus Nein, modal, Ton, nach 10 s RESULT 8')
print('Uebungen geschrieben')
