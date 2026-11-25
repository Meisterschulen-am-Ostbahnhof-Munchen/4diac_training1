"""Erzeugt die Lib isobus_UT_dialog-3.0.0 in training1.

Aufruf: python gen_dialog_lib.py <training1_root>
Liest die Objekt-IDs aus Workspace_Dialog/DefaultPool/Output/DefaultPool.iop.h.
"""
import re, sys
from pathlib import Path
from xml.sax.saxutils import escape

root = Path(sys.argv[1]) / 'Ventilsteuerung'
lib = root / '4diacIDE-workspace' / '.lib' / 'isobus_UT_dialog-3.0.0'
iop_h = root / 'ISO-DesignerProjects' / 'Workspace_Dialog' / 'DefaultPool' / 'Output' / 'DefaultPool.iop.h'
PKG = 'isobus::UT::dialog'
DATE = '2026-11-17'
COPY = ('Copyright (c) 2026 Meisterschulen am Ostbahnhof  &#10; &#10;This program and the accompanying materials are made  &#10;'
        'available under the terms of the Eclipse Public License 2.0  &#10;which is available at https://www.eclipse.org/legal/epl-2.0/  &#10; &#10;'
        'SPDX-License-Identifier: EPL-2.0')
HDR_ID = f'\t<Identification Standard="61499-2" Description="{COPY}">\n\t</Identification>\n'
HDR_VER = (f'\t<VersionInfo Organization="Meisterschulen am Ostbahnhof" Version="1.0" Author="Franz Höpfinger" '
           f'Date="{DATE}" Remarks="initial API and implementation and/or initial documentation">\n\t</VersionInfo>\n')

ids = {m.group(1): int(m.group(2)) for m in re.finditer(r'#define\s+(\w+)\s+(\d+)', iop_h.read_text(encoding='utf-8', errors='replace'))}
LIB_IDS = ['Container_Dialog', 'Container_Dlg_Box', 'Rectangle_Dlg_Cover', 'FillAttributes_Dlg_Title',
           'ObjectPointer_Dlg_Cover', 'ObjectPointer_Dlg_Icon', 'ObjectPointer_Dlg_Title', 'ObjectPointer_Dlg_Text',
           'ObjectPointer_Dlg_Buttons',
           'Container_Dlg_Icon_Info', 'Container_Dlg_Icon_Question', 'Container_Dlg_Icon_Warning', 'Container_Dlg_Icon_Error',
           'OutputString_Dlg_Title_Info', 'OutputString_Dlg_Title_Question', 'OutputString_Dlg_Title_Warning', 'OutputString_Dlg_Title_Error',
           'Container_Dlg_Buttons_OK', 'Container_Dlg_Buttons_OKCancel', 'Container_Dlg_Buttons_AbortRetryIgnore',
           'Container_Dlg_Buttons_YesNoCancel', 'Container_Dlg_Buttons_YesNo', 'Container_Dlg_Buttons_RetryCancel',
           'Button_Dlg_OK', 'Button_Dlg_Cancel', 'Button_Dlg_Abort', 'Button_Dlg_Retry', 'Button_Dlg_Ignore',
           'Button_Dlg_Yes', 'Button_Dlg_No']
missing = [n for n in LIB_IDS if n not in ids]
assert not missing, missing
I = {n: ids[n] for n in LIB_IDS}
BTN = ['OK', 'Cancel', 'Abort', 'Retry', 'Ignore', 'Yes', 'No']           # Index 0..6 = KeyCode-1 = RESULT-1
assert [I[f'Button_Dlg_{b}'] for b in BTN] == list(range(I['Button_Dlg_OK'], I['Button_Dlg_OK'] + 7))

def write(rel, text):
    p = lib / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')

# ------------------------------------------------------------------ Projekt
deps = [('core', 'core-3.0.0', '3.0.0'), ('events', 'events-3.0.0', '3.0.0'),
        ('isobus_UT', 'isobus_UT-3.0.0', '3.1.1'), ('isobus_UT_io', 'isobus_UT_io-3.0.0', '3.0.1')]
links = ''.join(f'\t\t<link>\n\t\t\t<name>External Libraries/{n}</name>\n\t\t\t<type>2</type>\n'
                f'\t\t\t<locationURI>WORKSPACE_LOC/.lib/{d}/typelib</locationURI>\n\t\t</link>\n' for n, d, _ in deps)
links += ''.join(f'\t\t<link>\n\t\t\t<name>External Libraries/{n}/MANIFEST.MF</name>\n\t\t\t<type>1</type>\n'
                 f'\t\t\t<locationURI>WORKSPACE_LOC/.lib/{d}/MANIFEST.MF</locationURI>\n\t\t</link>\n' for n, d, _ in deps)
write('.project', f'''<?xml version="1.0" encoding="UTF-8"?>
<projectDescription>
	<name>isobus_UT_dialog-3.0.0</name>
	<comment></comment>
	<projects>
	</projects>
	<buildSpec>
		<buildCommand>
			<name>org.eclipse.fordiac.ide.library.builder</name>
			<arguments>
			</arguments>
		</buildCommand>
		<buildCommand>
			<name>org.eclipse.xtext.ui.shared.xtextBuilder</name>
			<arguments>
			</arguments>
		</buildCommand>
		<buildCommand>
			<name>org.eclipse.fordiac.ide.export.builder</name>
			<arguments>
			</arguments>
		</buildCommand>
	</buildSpec>
	<natures>
		<nature>org.eclipse.fordiac.ide.systemmanagement.FordiacNature</nature>
		<nature>org.eclipse.xtext.ui.shared.xtextNature</nature>
	</natures>
	<linkedResources>
		<link>
			<name>External Libraries</name>
			<type>2</type>
			<locationURI>virtual:/virtual</locationURI>
		</link>
		<link>
			<name>Standard Libraries</name>
			<type>2</type>
			<locationURI>virtual:/virtual</locationURI>
		</link>
{links}	</linkedResources>
</projectDescription>
''')
write('.settings/org.eclipse.core.resources.prefs', 'eclipse.preferences.version=1\nencoding/<project>=UTF-8\n')
write('.settings/org.eclipse.fordiac.ide.gef.prefs', 'PinLabelStyle=PinLabelStyle_PinComment\nProjectStoreActive=true\neclipse.preferences.version=1\n')
req = ''.join(f'    <Required SymbolicName="{n}" Version="{v}"/>\n' for n, _, v in deps)
write('MANIFEST.MF', f'''<?xml version="1.0" encoding="UTF-8"?>
<Manifest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="platform:/resource/org.eclipse.fordiac.ide.library.model/model/library.xsd" Scope="Library">
  <Dependencies>
{req}  </Dependencies>
  <Product Comment="VT-Dialoge wie Windows-MessageBox: Container auf der aktuellen DataMask, Tasten, Icon, Timeout, modal/nicht modal. Pool-Vorlage: ISO-DesignerProjects/Workspace_Dialog (feste IDs, siehe DialogIDs.gcf)." Name="isobus_UT_dialog" SymbolicName="isobus_UT_dialog">
    <VersionInfo Author="Franz Höpfinger" Date="{DATE}" Version="3.0.0"/>
  </Product>
</Manifest>
''')

# ------------------------------------------------------------------ GCF
def gcf(name, comment, consts, header):
    xml = ''.join(f'\t\t<VarDeclaration Name="{n}" Type="{t}" Comment="{escape(c)}" InitialValue="{v}"/>\n' for n, t, v, c in consts)
    src = ''.join(f'\t\t{n} : {t} := {v}; // {c}\n' for n, t, v, c in consts)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<GlobalConstants Name="{name}" Comment="{comment}">\n{HDR_ID}{HDR_VER}'
            f'\t<CompilerInfo packageName="{PKG}">\n\t</CompilerInfo>\n\t<GlobalConstants>\n{xml}\t</GlobalConstants>\n'
            f'\t<OriginalSource><![CDATA[(* {header} *)\nPACKAGE {PKG};\n\nGLOBALCONSTANTS {name}\n\tVAR_GLOBAL CONSTANT\n{src}'
            f'\tEND_VAR\nEND_GLOBALCONSTANTS\n]]></OriginalSource>\n\t<Attribute Name="eclipse4diac::core::TypeHash" Value="\'\'"/>\n</GlobalConstants>\n')

write('typelib/DialogIDs.gcf', gcf('DialogIDs', 'Objekt-IDs der Dialog-Vorlage',
      [(n, 'UINT', f'UINT#{I[n]}', 'Vorlage Workspace_Dialog') for n in LIB_IDS],
      'Feste IDs aus ISO-DesignerProjects/Workspace_Dialog. Projekte uebernehmen die Vorlage mit denselben IDs.'))
consts = [('DLG_BTN_NONE', 0, 'keine Tasten (Toast)'), ('DLG_BTN_OK', 1, 'OK'), ('DLG_BTN_OKCANCEL', 2, 'OK, Abbrechen'),
          ('DLG_BTN_ABORTRETRYIGNORE', 3, 'Abbrechen, Wiederholen, Ignorieren'), ('DLG_BTN_YESNOCANCEL', 4, 'Ja, Nein, Abbrechen'),
          ('DLG_BTN_YESNO', 5, 'Ja, Nein'), ('DLG_BTN_RETRYCANCEL', 6, 'Wiederholen, Abbrechen'),
          ('DLG_ICON_NONE', 0, 'kein Icon'), ('DLG_ICON_INFO', 1, 'Information'), ('DLG_ICON_QUESTION', 2, 'Frage'),
          ('DLG_ICON_WARNING', 3, 'Warnung'), ('DLG_ICON_ERROR', 4, 'Fehler'),
          ('DLG_RES_NONE', 0, 'geschlossen/ersetzt'), ('DLG_RES_OK', 1, 'OK'), ('DLG_RES_CANCEL', 2, 'Abbrechen'),
          ('DLG_RES_ABORT', 3, 'Abbruch'), ('DLG_RES_RETRY', 4, 'Wiederholen'), ('DLG_RES_IGNORE', 5, 'Ignorieren'),
          ('DLG_RES_YES', 6, 'Ja'), ('DLG_RES_NO', 7, 'Nein'), ('DLG_RES_TIMEOUT', 8, 'Zeit abgelaufen')]
write('typelib/DialogConst.gcf', gcf('DialogConst', 'Konstanten fuer BUTTONS, ICON, RESULT',
      [(n, 'USINT', f'USINT#{v}', c) for n, v, c in consts],
      'Werte wie Windows MessageBox (Tasten, Icon, Ergebnis). RESULT = KeyCode des Dialog-Buttons.'))

# ------------------------------------------------------------------ DLG_CTRL (Basic FB)
def ev(name, typ, comment, withs=()):
    w = ''.join(f'\t\t\t\t<With Var="{x}"/>\n' for x in withs)
    return f'\t\t\t<Event Name="{name}" Type="{typ}" Comment="{escape(comment)}">\n{w}\t\t\t</Event>\n'

def var(name, typ, comment, init=None):
    iv = f' InitialValue="{init}"' if init is not None else ''
    return f'\t\t\t<VarDeclaration Name="{name}" Type="{typ}" Comment="{escape(comment)}"{iv}/>\n'

SHOW_IN = ['TEXT_ID', 'TITLE_ID', 'ICON', 'BUTTONS', 'DEFAULT_BUTTON', 'MODAL', 'TIMEOUT', 'AUDIO']
SHOW_OUT = ['COVER_ID', 'ICON_ID', 'TITLE_ID_O', 'TEXT_ID_O', 'BUTTONS_ID', 'TITLE_COLOUR', 'FOCUS_K', 'AUDIO_O']
ev_in = (ev('INIT', 'EInit', 'Initialisierung', ['QI']) + ev('SHOW', 'Event', 'Dialog zeigen', SHOW_IN)
         + ev('CLOSE', 'Event', 'Dialog vom Programm schliessen') + ev('SHOWN', 'Event', 'Anzeige-Kette fertig')
         + ev('HIDDEN', 'Event', 'Ausblenden fertig') + ev('TMO', 'Event', 'Zeit abgelaufen')
         + ''.join(ev(f'B_{b.upper()}', 'Event', f'Button {b} losgelassen') for b in BTN))
ev_out = (ev('INITO', 'EInit', 'Initialisierung fertig', ['QO']) + ev('SHOWO', 'Event', 'Anzeige-Kette starten', SHOW_OUT)
          + ev('HIDEO', 'Event', 'Dialog ausblenden') + ev('START_T', 'Event', 'Timeout starten', ['TIMEOUT_O'])
          + ev('STOP_T', 'Event', 'Timeout stoppen') + ev('CNF', 'Event', 'Dialog beendet', ['QO', 'RESULT']))
v_in = (var('QI', 'BOOL', 'Freigabe', 'TRUE') + var('TEXT_ID', 'UINT', 'OutputString Meldungstext', 'UINT#65535')
        + var('TITLE_ID', 'UINT', 'OutputString Titel, NULL = Standard je Icon', 'UINT#65535')
        + var('ICON', 'USINT', 'DLG_ICON_*', 'USINT#1') + var('BUTTONS', 'USINT', 'DLG_BTN_*', 'USINT#1')
        + var('DEFAULT_BUTTON', 'USINT', 'Fokus auf Taste 1..3', 'USINT#1') + var('MODAL', 'BOOL', 'Maske abdecken', 'FALSE')
        + var('TIMEOUT', 'TIME', 'T#0s = kein Timeout', 'T#0s') + var('AUDIO', 'BOOL', 'Ton beim Oeffnen', 'FALSE'))
v_out = (var('QO', 'BOOL', 'Qualitaet') + var('RESULT', 'USINT', 'DLG_RES_*')
         + var('COVER_ID', 'UDINT', 'Ziel ObjectPointer_Dlg_Cover') + var('ICON_ID', 'UDINT', 'Ziel ObjectPointer_Dlg_Icon')
         + var('TITLE_ID_O', 'UDINT', 'Ziel ObjectPointer_Dlg_Title') + var('TEXT_ID_O', 'UDINT', 'Ziel ObjectPointer_Dlg_Text')
         + var('BUTTONS_ID', 'UDINT', 'Ziel ObjectPointer_Dlg_Buttons') + var('TITLE_COLOUR', 'USINT', 'VT-Farbindex Titelzeile')
         + var('FOCUS_K', 'UINT', 'Fokus-Button 0..6, 7 = keiner') + var('AUDIO_O', 'BOOL', 'Ton ja/nein')
         + var('TIMEOUT_O', 'TIME', 'Timeout'))
v_int = (var('xPendingShow', 'BOOL', 'neues SHOW wartet') + var('xPendingClose', 'BOOL', 'Schliessen wartet'))

N = 65535
prep = f'''(* Pointer-Ziele aus der Vorlage Workspace_Dialog, IDs siehe DialogIDs.gcf *)
IF MODAL THEN COVER_ID := {I['Rectangle_Dlg_Cover']}; ELSE COVER_ID := {N}; END_IF;
CASE ICON OF
  1: ICON_ID := {I['Container_Dlg_Icon_Info']}; TITLE_COLOUR := 2;      (* gruen *)
  2: ICON_ID := {I['Container_Dlg_Icon_Question']}; TITLE_COLOUR := 15; (* navy *)
  3: ICON_ID := {I['Container_Dlg_Icon_Warning']}; TITLE_COLOUR := 6;   (* oliv *)
  4: ICON_ID := {I['Container_Dlg_Icon_Error']}; TITLE_COLOUR := 12;    (* rot *)
ELSE
  ICON_ID := {N}; TITLE_COLOUR := 2;
END_CASE;
IF TITLE_ID <> {N} THEN
  TITLE_ID_O := UINT_TO_UDINT(TITLE_ID);
ELSIF ICON >= 1 AND ICON <= 4 THEN
  TITLE_ID_O := {I['OutputString_Dlg_Title_Info'] - 1} + USINT_TO_UDINT(ICON);
ELSE
  TITLE_ID_O := {I['OutputString_Dlg_Title_Info']};
END_IF;
TEXT_ID_O := UINT_TO_UDINT(TEXT_ID);
(* FOCUS_K: 0 OK, 1 Cancel, 2 Abort, 3 Retry, 4 Ignore, 5 Yes, 6 No, 7 kein Fokus *)
FOCUS_K := 7;
CASE BUTTONS OF
  1: BUTTONS_ID := {I['Container_Dlg_Buttons_OK']}; FOCUS_K := 0;
  2: BUTTONS_ID := {I['Container_Dlg_Buttons_OKCancel']};
     IF DEFAULT_BUTTON = 2 THEN FOCUS_K := 1; ELSE FOCUS_K := 0; END_IF;
  3: BUTTONS_ID := {I['Container_Dlg_Buttons_AbortRetryIgnore']};
     IF DEFAULT_BUTTON = 2 THEN FOCUS_K := 3; ELSIF DEFAULT_BUTTON = 3 THEN FOCUS_K := 4; ELSE FOCUS_K := 2; END_IF;
  4: BUTTONS_ID := {I['Container_Dlg_Buttons_YesNoCancel']};
     IF DEFAULT_BUTTON = 2 THEN FOCUS_K := 6; ELSIF DEFAULT_BUTTON = 3 THEN FOCUS_K := 1; ELSE FOCUS_K := 5; END_IF;
  5: BUTTONS_ID := {I['Container_Dlg_Buttons_YesNo']};
     IF DEFAULT_BUTTON = 2 THEN FOCUS_K := 6; ELSE FOCUS_K := 5; END_IF;
  6: BUTTONS_ID := {I['Container_Dlg_Buttons_RetryCancel']};
     IF DEFAULT_BUTTON = 2 THEN FOCUS_K := 1; ELSE FOCUS_K := 3; END_IF;
ELSE
  BUTTONS_ID := {N};
END_CASE;
TIMEOUT_O := TIMEOUT;
AUDIO_O := AUDIO;
xPendingShow := FALSE;
xPendingClose := FALSE;'''

algs = {'INIT_ALG': 'QO := QI;\nRESULT := 0;\nxPendingShow := FALSE;\nxPendingClose := FALSE;',
        'PREP': prep, 'R_NONE': 'RESULT := 0;', 'R_TMO': 'RESULT := 8;',
        'MARK_SHOW': 'xPendingShow := TRUE;', 'MARK_CLOSE': 'xPendingClose := TRUE;'}
for n, b in enumerate(BTN):
    algs[f'R_{b.upper()}'] = f'RESULT := {n + 1};'

states, trans = [], []
def st(name, actions=(), comment=''):
    a = ''.join(f'\t\t\t\t<ECAction Algorithm="{al}"/>\n' if al and not out else
                (f'\t\t\t\t<ECAction Algorithm="{al}" Output="{out}"/>\n' if al else f'\t\t\t\t<ECAction Output="{out}"/>\n')
                for al, out in actions)
    x, y = 400 + (len(states) % 6) * 1400, 300 + (len(states) // 6) * 900
    states.append(f'\t\t\t<ECState Name="{name}" Comment="{escape(comment)}" x="{x}" y="{y}">\n{a}\t\t\t</ECState>\n')
def tr(src, dst, cond):
    trans.append(f'\t\t\t<ECTransition Source="{src}" Destination="{dst}" Condition="{escape(cond)}" x="0" y="0"/>\n')

st('START', comment='Initial State')
st('S_INIT', [('INIT_ALG', 'INITO')])
st('IDLE', comment='kein Dialog offen')
st('S_PREP', [('PREP', 'SHOWO')], 'Anzeige-Kette starten')
st('OPENING', comment='Anzeige-Kette laeuft')
st('S_O_SHOW', [('MARK_SHOW', None)])
st('S_O_CLOSE', [('R_NONE', None), ('MARK_CLOSE', None)])
st('S_REPLACE', [('R_NONE', 'CNF')], 'alter Dialog ersetzt')
st('S_START_T', [(None, 'START_T')])
st('OPEN', comment='Dialog sichtbar')
for b in BTN:
    st(f'S_R_{b.upper()}', [(f'R_{b.upper()}', None)])
st('S_R_TMO', [('R_TMO', None)])
st('S_R_CLOSE', [('R_NONE', None)])
st('S_REPLACE_OPEN', [('R_NONE', 'STOP_T'), (None, 'CNF')], 'neues SHOW waehrend offen')
st('S_HIDE', [(None, 'STOP_T'), (None, 'HIDEO')])
st('CLOSING', comment='Ausblenden laeuft')
st('S_C_SHOW', [('MARK_SHOW', None)])
st('S_DONE_SHOW', [(None, 'CNF')])
st('S_DONE', [(None, 'CNF')])

tr('START', 'S_INIT', 'INIT')
tr('S_INIT', 'IDLE', '1')
tr('IDLE', 'S_INIT', 'INIT')
tr('IDLE', 'S_PREP', 'SHOW')
tr('S_PREP', 'OPENING', '1')
tr('OPENING', 'S_HIDE', 'SHOWN[xPendingClose]')
tr('OPENING', 'S_REPLACE', 'SHOWN[xPendingShow]')
tr('OPENING', 'S_START_T', 'SHOWN[TIMEOUT_O > T#0s]')
tr('OPENING', 'OPEN', 'SHOWN')
tr('OPENING', 'S_O_SHOW', 'SHOW')
tr('OPENING', 'S_O_CLOSE', 'CLOSE')
tr('S_O_SHOW', 'OPENING', '1')
tr('S_O_CLOSE', 'OPENING', '1')
tr('S_REPLACE', 'S_PREP', '1')
tr('S_START_T', 'OPEN', '1')
for b in BTN:
    tr('OPEN', f'S_R_{b.upper()}', f'B_{b.upper()}')
    tr(f'S_R_{b.upper()}', 'S_HIDE', '1')
tr('OPEN', 'S_R_TMO', 'TMO')
tr('S_R_TMO', 'S_HIDE', '1')
tr('OPEN', 'S_R_CLOSE', 'CLOSE')
tr('S_R_CLOSE', 'S_HIDE', '1')
tr('OPEN', 'S_REPLACE_OPEN', 'SHOW')
tr('S_REPLACE_OPEN', 'S_PREP', '1')
tr('S_HIDE', 'CLOSING', '1')
tr('CLOSING', 'S_DONE_SHOW', 'HIDDEN[xPendingShow]')
tr('CLOSING', 'S_DONE', 'HIDDEN')
tr('CLOSING', 'S_C_SHOW', 'SHOW')
tr('S_C_SHOW', 'CLOSING', '1')
tr('S_DONE_SHOW', 'S_PREP', '1')
tr('S_DONE', 'IDLE', '1')

alg_xml = ''.join(f'\t\t<Algorithm Name="{n}">\n\t\t\t<ST><![CDATA[{b}]]></ST>\n\t\t</Algorithm>\n' for n, b in algs.items())
write('typelib/DLG_CTRL.fbt', f'''<?xml version="1.0" encoding="UTF-8"?>
<FBType Name="DLG_CTRL" Comment="Ablaufsteuerung eines VT-Dialogs (MessageBox)">
{HDR_ID}{HDR_VER}	<CompilerInfo packageName="{PKG}">
	</CompilerInfo>
	<InterfaceList>
		<EventInputs>
{ev_in}		</EventInputs>
		<EventOutputs>
{ev_out}		</EventOutputs>
		<InputVars>
{v_in}		</InputVars>
		<OutputVars>
{v_out}		</OutputVars>
	</InterfaceList>
	<BasicFB>
		<InternalVars>
{v_int}		</InternalVars>
		<ECC>
{''.join(states)}{''.join(trans)}		</ECC>
{alg_xml}	</BasicFB>
	<Attribute Name="eclipse4diac::core::TypeHash" Value="''"/>
</FBType>
''')

# ------------------------------------------------------------------ SubApps
class Net:
    def __init__(self):
        self.fbs, self.ev, self.data, self.imports = [], [], [], set()
    def fb(self, name, typ, x, y, params=()):
        p = ''.join(f'\t\t\t<Parameter Name="{k}" Value="{escape(v)}"/>\n' for k, v in params)
        self.fbs.append(f'\t\t<FB Name="{name}" Type="{typ}" x="{x}" y="{y}">\n{p}\t\t</FB>\n')
    def e(self, s, d):
        self.ev.append(f'\t\t\t<Connection Source="{s}" Destination="{d}"/>\n')
    def d(self, s, d):
        self.data.append(f'\t\t\t<Connection Source="{s}" Destination="{d}"/>\n')

def subapp(name, comment, ev_in, ev_out, vin, vout, net):
    imp = ''.join(f'\t\t<Import declaration="{i}"/>\n' for i in sorted(net.imports))
    def se(n, t, c):
        return f'\t\t\t\t<SubAppEvent Name="{n}" Type="{t}" Comment="{escape(c)}">\n\t\t\t\t</SubAppEvent>\n'
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<SubAppType Name="{name}" Comment="{escape(comment)}">
{HDR_ID}{HDR_VER}	<CompilerInfo packageName="{PKG}">
{imp}	</CompilerInfo>
	<SubAppInterfaceList>
		<SubAppEventInputs>
{''.join(se(*e) for e in ev_in)}		</SubAppEventInputs>
		<SubAppEventOutputs>
{''.join(se(*e) for e in ev_out)}		</SubAppEventOutputs>
		<InputVars>
{''.join(var(*v).replace(chr(9) * 3, chr(9) * 3) for v in vin)}		</InputVars>
		<OutputVars>
{''.join(var(*v) for v in vout)}		</OutputVars>
	</SubAppInterfaceList>
	<SubAppNetwork>
{''.join(net.fbs)}		<EventConnections>
{''.join(net.ev)}		</EventConnections>
		<DataConnections>
{''.join(net.data)}		</DataConnections>
	</SubAppNetwork>
</SubAppType>
'''

Q = 'isobus::UT::Q::'
n = Net()
def imp(c):
    n.imports.add(f'{PKG}::DialogIDs::{c}')
    return c
n.imports.add('isobus::UT::Q::const::IDs::ID_NULL')
n.imports.add('isobus::UT::io::Button::ButtonActivationCode::BT_RELEASED_UNLATCHED')

n.fb('CTRL', f'{PKG}::DLG_CTRL', 0, 0)
ptrs = [('QN_COVER', 'ObjectPointer_Dlg_Cover', 'COVER_ID'), ('QN_ICON', 'ObjectPointer_Dlg_Icon', 'ICON_ID'),
        ('QN_TITLE', 'ObjectPointer_Dlg_Title', 'TITLE_ID_O'), ('QN_TEXT', 'ObjectPointer_Dlg_Text', 'TEXT_ID_O'),
        ('QN_BUTTONS', 'ObjectPointer_Dlg_Buttons', 'BUTTONS_ID')]
for k, (fbn, obj, out) in enumerate(ptrs):
    n.fb(fbn, Q + 'Q_NumericValue', 3000, -4000 + k * 1600, [('QI', 'TRUE'), ('u16ObjId', imp(obj))])
    n.d(f'CTRL.{out}', f'{fbn}.u32NewValue')
n.fb('QF_TITLE', Q + 'Q_FillAttributes', 3000, 4200,
     [('QI', 'TRUE'), ('u16ObjId', imp('FillAttributes_Dlg_Title')), ('u8FillType', 'USINT#2'), ('u16FillPatternId', 'ID_NULL')])
n.d('CTRL.TITLE_COLOUR', 'QF_TITLE.u8FillColour')
n.fb('QH_SHOW', Q + 'Q_ObjHideShow', 6000, -4000, [('QI', 'TRUE'), ('u16ObjId', imp('Container_Dialog')), ('qVisible', 'BYTE#1')])
n.fb('QH_HIDE', Q + 'Q_ObjHideShow', 6000, 6000, [('QI', 'TRUE'), ('u16ObjId', 'Container_Dialog'), ('qVisible', 'BYTE#0')])
n.fb('FOCUS', 'iec61499::events::E_DEMUX_8', 6000, -2000)
n.d('CTRL.FOCUS_K', 'FOCUS.K')
for k, b in enumerate(BTN):
    n.fb(f'QS_{b.upper()}', Q + 'Q_ObjSelectInput', 9000, -4000 + k * 1400,
         [('QI', 'TRUE'), ('u16ObjId', imp(f'Button_Dlg_{b}')), ('u8Option', 'USINT#255')])
n.fb('FOCUS_DONE', 'iec61499::events::E_MUX_8', 12000, -2000)
n.fb('AUDIO_SW', 'iec61499::events::E_SWITCH', 14500, -2000)
n.d('CTRL.AUDIO_O', 'AUDIO_SW.G')
n.fb('Q_AUDIO', Q + 'Q_CtrlAudioSignal', 17000, -1000,
     [('QI', 'TRUE'), ('u8NumOfRepit', 'USINT#1'), ('u16Frequency', 'UINT#2000'), ('u16OnTimeMs', 'UINT#100'), ('u16OffTimeMs', 'UINT#0')])
n.fb('AUDIO_DONE', 'iec61499::events::E_MERGE', 20000, -2000)
n.fb('TIMER', 'iec61499::events::E_DELAY', 3000, 7000)
n.d('CTRL.TIMEOUT_O', 'TIMER.DT')
for k, b in enumerate(BTN):
    n.fb(f'BTN_{b.upper()}', 'isobus::UT::io::Button::Button_IE', -4000, -4000 + k * 1600,
         [('QI', 'TRUE'), ('u16ObjId', f'Button_Dlg_{b}'), ('InputEvent', 'BT_RELEASED_UNLATCHED')])
    n.e(f'BTN_{b.upper()}.IND', f'CTRL.B_{b.upper()}')

# Anzeige-Kette
chain = ['CTRL.SHOWO'] + [f'{p[0]}' for p in ptrs] + ['QF_TITLE', 'QH_SHOW']
n.e('CTRL.SHOWO', 'QN_COVER.REQ')
seq = [p[0] for p in ptrs] + ['QF_TITLE', 'QH_SHOW']
for a, b in zip(seq, seq[1:]):
    n.e(f'{a}.CNF', f'{b}.REQ')
n.e('QH_SHOW.CNF', 'FOCUS.EI')
for k, b in enumerate(BTN):
    n.e(f'FOCUS.EO{k + 1}', f'QS_{b.upper()}.REQ')
    n.e(f'QS_{b.upper()}.CNF', f'FOCUS_DONE.EI{k + 1}')
n.e('FOCUS.EO8', 'FOCUS_DONE.EI8')
n.e('FOCUS_DONE.EO', 'AUDIO_SW.EI')
n.e('AUDIO_SW.EO0', 'AUDIO_DONE.EI1')
n.e('AUDIO_SW.EO1', 'Q_AUDIO.REQ')
n.e('Q_AUDIO.CNF', 'AUDIO_DONE.EI2')
n.e('AUDIO_DONE.EO', 'CTRL.SHOWN')
# Ausblenden, Timer
n.e('CTRL.HIDEO', 'QH_HIDE.REQ')
n.e('QH_HIDE.CNF', 'CTRL.HIDDEN')
n.e('CTRL.START_T', 'TIMER.START')
n.e('CTRL.STOP_T', 'TIMER.STOP')
n.e('TIMER.EO', 'CTRL.TMO')
# INIT-Kette
init_seq = ['CTRL'] + [p[0] for p in ptrs] + ['QF_TITLE', 'QH_SHOW', 'QH_HIDE'] + [f'QS_{b.upper()}' for b in BTN] \
           + ['Q_AUDIO'] + [f'BTN_{b.upper()}' for b in BTN]
n.e('INIT', 'CTRL.INIT')
for a, b in zip(init_seq, init_seq[1:]):
    n.e(f'{a}.INITO', f'{b}.INIT')
n.e(f'{init_seq[-1]}.INITO', 'INITO')
# Schnittstelle
n.e('SHOW', 'CTRL.SHOW')
n.e('CLOSE', 'CTRL.CLOSE')
n.e('CTRL.CNF', 'CNF')
for v in ['QI'] + SHOW_IN:
    n.d(v, f'CTRL.{v}')
n.d('CTRL.QO', 'QO')
n.d('CTRL.RESULT', 'RESULT')

VIN = [('QI', 'BOOL', 'Freigabe', 'TRUE'), ('TEXT_ID', 'UINT', 'OutputString Meldungstext', 'ID_NULL'),
       ('TITLE_ID', 'UINT', 'OutputString Titel, NULL = Standard je Icon', 'ID_NULL'),
       ('ICON', 'USINT', 'DLG_ICON_*', 'USINT#1'), ('BUTTONS', 'USINT', 'DLG_BTN_*', 'USINT#1'),
       ('DEFAULT_BUTTON', 'USINT', 'Fokus auf Taste 1..3', 'USINT#1'), ('MODAL', 'BOOL', 'Maske abdecken', 'FALSE'),
       ('TIMEOUT', 'TIME', 'T#0s = kein Timeout', 'T#0s'), ('AUDIO', 'BOOL', 'Ton beim Oeffnen', 'FALSE')]
VOUT = [('QO', 'BOOL', 'Qualitaet'), ('RESULT', 'USINT', 'DLG_RES_*')]
write('typelib/DLG_MessageBox.SUB', subapp(
    'DLG_MessageBox', 'VT-Dialog wie Windows-MessageBox (eine Instanz je Anwendung)',
    [('INIT', 'EInit', 'Initialisierung'), ('SHOW', 'Event', 'Dialog zeigen'), ('CLOSE', 'Event', 'Dialog schliessen')],
    [('INITO', 'EInit', 'Initialisierung fertig'), ('CNF', 'Event', 'Dialog beendet, RESULT gueltig')],
    VIN, VOUT, n))

# DLG_Toast: Huelle mit festen Werten
t = Net()
t.imports.add('isobus::UT::Q::const::IDs::ID_NULL')
t.fb('MSG', f'{PKG}::DLG_MessageBox', 0, 0, [('BUTTONS', 'USINT#0'), ('DEFAULT_BUTTON', 'USINT#1'), ('MODAL', 'FALSE'), ('AUDIO', 'FALSE')])
for v in ['QI', 'TEXT_ID', 'TITLE_ID', 'ICON', 'TIMEOUT']:
    t.d(v, f'MSG.{v}')
t.d('MSG.QO', 'QO')
t.e('INIT', 'MSG.INIT'); t.e('MSG.INITO', 'INITO'); t.e('SHOW', 'MSG.SHOW'); t.e('CLOSE', 'MSG.CLOSE'); t.e('MSG.CNF', 'CNF')
write('typelib/DLG_Toast.SUB', subapp(
    'DLG_Toast', 'Hinweis ohne Tasten, verschwindet nach TIMEOUT',
    [('INIT', 'EInit', 'Initialisierung'), ('SHOW', 'Event', 'Hinweis zeigen'), ('CLOSE', 'Event', 'Hinweis schliessen')],
    [('INITO', 'EInit', 'Initialisierung fertig'), ('CNF', 'Event', 'Hinweis beendet')],
    [('QI', 'BOOL', 'Freigabe', 'TRUE'), ('TEXT_ID', 'UINT', 'OutputString Meldungstext', 'ID_NULL'),
     ('TITLE_ID', 'UINT', 'OutputString Titel, NULL = Standard', 'ID_NULL'), ('ICON', 'USINT', 'DLG_ICON_*', 'USINT#1'),
     ('TIMEOUT', 'TIME', 'Anzeigedauer', 'T#3s')],
    [('QO', 'BOOL', 'Qualitaet')], t))
print('Lib geschrieben:', lib)
