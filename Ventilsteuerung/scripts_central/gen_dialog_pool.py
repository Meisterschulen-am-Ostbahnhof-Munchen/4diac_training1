"""Erzeugt die Dialog-Vorlage (isobus_UT_dialog) im Pool Workspace_Dialog.

Aufruf: python gen_dialog_pool.py <pool_dir>
Erwartet einen frischen Pool aus Workspace_Empty (DataMask_M1, SoftKeyMask_S1, SoftKey_F1),
ohne DefaultPool.jops (sonst hängt ISODesigner /Compile). Danach den Pool bauen.
"""
import base64, random, re, sys
from pathlib import Path

pool = Path(sys.argv[1])
jop_p = pool / 'DefaultPool.jop'
jop = jop_p.read_text(encoding='utf-8')
random.seed(4711)

def enc(s):
    return base64.b64encode((s + '\0').encode('utf-16le')).decode()

def prop(name, value, cdata=False):
    if cdata:
        return f'\t\t\t\t<Property Name="{name}">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[{value}]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
    if value == '':
        return f'\t\t\t\t<Property Name="{name}">\n\t\t\t\t\t<Value/>\n\t\t\t\t</Property>\n'
    return f'\t\t\t\t<Property Name="{name}">\n\t\t\t\t\t<Value>{value}</Value>\n\t\t\t\t</Property>\n'

def tail_props():
    return (prop('Visible', 1) + prop('Locked', 0) + prop('Comment', 'AAA=', True)
            + prop('Disabled', 0) + prop('ExternalReferenceAllowed', 0))

def objects(ids):
    if not ids:
        return ''
    return '\t\t\t<Objects>\n' + ''.join(f'\t\t\t\t<Object JVS-ID="{i}"/>\n' for i in ids) + '\t\t\t</Objects>\n'

def obj(cls, name, oname, jid, sheet, props, children, pinned=False, extra=''):
    pn = 'TRUE' if pinned else 'FALSE'
    return (f'\t\t<Object Class="{cls}" Name="{name}" ObjectName="{oname}" Pinned="{pn}" JVS-ID="{jid}">\n'
            f'\t\t\t<PropertySheet Name="{sheet}">\n{props}\t\t\t</PropertySheet>\n{extra}{objects(children)}\t\t</Object>\n')

out = []
next_proxy = max(int(x) for x in re.findall(r'Class="CProxy"[^>]*JVS-ID="(\d+)"', jop)) + 1

def proxy(target, left, top, name='Proxy'):
    global next_proxy
    pid = next_proxy
    next_proxy += 1
    p = (prop('Top', top) + prop('Left', left) + prop('Name', name) + prop('TabIndex', -1)
         + prop('Transform', f'(1.0000000000000000)(0.0000000000000000)({left:.16f})(0.0000000000000000)(1.0000000000000000)({top:.16f})'))
    out.append(obj('CProxy', name, '', pid, 'Proxy', p, [target]).replace('ObjectName="" ', 'ObjectName="" '))
    return pid

# ---------------------------------------------------------------- Attribute
def font(jid, oname, size, h, w, pw, color):
    p = (prop('Name', 'MS Shell Dlg') + prop('Size', size) + prop('Height', h) + prop('Color', color)
         + prop('Weight', 400) + prop('Italic', 0) + prop('Underline', 0) + prop('Strikeout', 0)
         + prop('PointWidth', pw) + prop('Width', w) + prop('Inverted', 0) + prop('FlashInverted', 0)
         + prop('FlashHidden', 0) + prop('Proportional', 0) + prop('ISOFontType', 0) + prop('ResourceID', '')
         + prop('Comment', 'AAA=', True))
    out.append(f'\t\t<Object Class="CFontStyle" JVS-ID="{jid}" ObjectName="{oname}" Pinned="FALSE">\n'
               f'\t\t\t<PropertySheet Name="Font">\n{p}\t\t\t</PropertySheet>\n\t\t</Object>\n')

def line_attr(jid, oname, color, width):
    p = (prop('Color', color) + prop('Style', 0) + prop('Width', width) + prop('Transparent', 0)
         + prop('LineArtBits', '1111111111111111') + prop('CapStyle', 0) + prop('Comment', 'AAA=', True))
    out.append(f'\t\t<Object Class="CLineStyle" Name="LineStyle" ObjectName="{oname}" Pinned="FALSE" JVS-ID="{jid}">\n'
               f'\t\t\t<PropertySheet Name="LineStyle">\n{p}\t\t\t</PropertySheet>\n\t\t</Object>\n')

def fill_attr(jid, oname, color):
    p = (prop('HatchStyle', 0) + prop('FillStyle', 0) + prop('BackColor', color) + prop('ForeColor', color)
         + prop('TransparentBackground', 1) + prop('FillTransparent', 0) + prop('FillType', 2)
         + prop('FillPatternObjectID', -1) + prop('GradientDirection', '0.000000')
         + prop('RadialRefPointIsCenter', 1) + prop('DistanceInPercentFromStart', '0.000000')
         + prop('Comment', 'AAA=', True))
    out.append(f'\t\t<Object Class="CFillStyle" Name="FillStyle" ObjectName="{oname}" Pinned="FALSE" JVS-ID="{jid}">\n'
               f'\t\t\t<PropertySheet Name="FillStyle">\n{p}\t\t\t</PropertySheet>\n\t\t</Object>\n')

# ---------------------------------------------------------------- Grafik
def rect(jid, oname, w, h, fill, line, pinned=False):
    pts = f'(0,0)({w},0)({w},{h})(0,{h})'
    p = (prop('LineSupression', '0000') + prop('RoundEdgeRadius', 0) + prop('Points', pts)
         + prop('OriginalPoints', pts)
         + prop('Transform', '(1.0000000000000000)(0.0000000000000000)(0.0000000000000000)(0.0000000000000000)(1.0000000000000000)(0.0000000000000000)')
         + prop('Width', w) + prop('Height', h) + tail_props())
    out.append(obj('CRectangle', 'Rectangle', oname, jid, 'Rectangle', p, [fill, line], pinned))

def ellipse(jid, oname, w, h, fill, line):
    p = (prop('StartAngle', 0) + prop('EndAngle', 0) + prop('Type', 0) + prop('Width', w)
         + prop('Height', h) + tail_props())
    out.append(obj('CEllipse', 'Ellipse', oname, jid, 'Ellipse', p, [fill, line]))

def text(jid, oname, s, w, h, fnt, align_h=0, align_v=0, transparent=1, bk=16777215, pinned=False):
    e = enc(s)
    p = (prop('Text', e, True) + prop('ResourceID', '') + prop('MultiLine', 1) + prop('WordBreak', 1)
         + prop('WrapOnHyphen', 0) + prop('AlignH', align_h) + prop('AlignV', align_v) + prop('Appearance', 0)
         + prop('ControlType', 0) + prop('Numeric', 0) + prop('Offset', 0) + prop('Scale', 1)
         + prop('FormatType', 0) + prop('FormatString', 0) + prop('NoOfDecimals', 0) + prop('Value', e, True)
         + prop('SetLengthAsMaximumLength', 0) + prop('StringLength', len(s)) + prop('Transparent', transparent)
         + prop('LeadingZeros', 0) + prop('ZeroAsBlank', 0) + prop('Truncate', 0) + prop('BkColor', bk)
         + prop('RoundEdgeRadius', 0) + prop('Width', w) + prop('Height', h) + tail_props())
    out.append(obj('COutputText', 'Text', oname, jid, 'Text', p, [fnt], pinned))

def group(jid, oname, w, h, children, hidden=0, pinned=False):
    p = prop('Hidden', hidden) + prop('ClipsChildren', 1) + prop('Width', w) + prop('Height', h) + tail_props()
    out.append(obj('CGroup', 'Group', oname, jid, 'Group', p, children, pinned))

def pointer(jid, oname, child_proxy=None):
    p = tail_props()
    out.append(obj('CPointer', 'Pointer', oname, jid, 'Pointer', p, [child_proxy] if child_proxy else []))

def button(jid, oname, keycode, w, h, children, back=12632256, events=''):
    p = (prop('BackColor', back) + prop('BorderColor', 0) + prop('KeyCode', keycode) + prop('Hotkey', 0)
         + prop('Latchable', 0) + prop('Latched', 0) + prop('SuppressBorder', 0) + prop('TransparentBackground', 0)
         + prop('Enabled', 1) + prop('NoBorder', 0) + prop('RoundEdgeRadius', 0) + prop('AutoAdjustTextarea', 0)
         + prop('3DStyle', 0) + prop('Width', w) + prop('Height', h) + tail_props())
    out.append(obj('CButton', 'Button', oname, jid, 'Button', p, children, extra=events))

def softkey(jid, oname, keycode, children, events=''):
    p = (prop('BackColor', 10066329) + prop('KeyCode', keycode) + prop('Hotkey', 0) + prop('Width', 80)
         + prop('Height', 80) + prop('Visible', 1) + prop('Comment', 'AAA=', True) + prop('Disabled', 0)
         + prop('ExternalReferenceAllowed', 0))
    out.append(obj('CSoftKey', 'SoftKey', oname, jid, 'SoftKey', p, children, extra=events))

def output_number(jid, oname, w, h, fnt):
    e = enc('0')
    p = (prop('Text', e, True) + prop('ResourceID', '') + prop('MultiLine', 0) + prop('WordBreak', 0)
         + prop('WrapOnHyphen', 0) + prop('AlignH', 2) + prop('AlignV', 0) + prop('Appearance', 0)
         + prop('ControlType', 0) + prop('Numeric', 1) + prop('Offset', 0) + prop('Scale', 1)
         + prop('FormatType', 0) + prop('FormatString', 0) + prop('NoOfDecimals', 0) + prop('Value', e, True)
         + prop('SetLengthAsMaximumLength', 0) + prop('StringLength', 4) + prop('Transparent', 0)
         + prop('LeadingZeros', 0) + prop('ZeroAsBlank', 0) + prop('Truncate', 0) + prop('BkColor', 16777215)
         + prop('RoundEdgeRadius', 0) + prop('Width', w) + prop('Height', h) + tail_props())
    out.append(obj('COutputNumber', 'Text', oname, jid, 'Text', p, [fnt]))

def macro_event(event_id, event_name, macro):
    def ep(n, v):
        return f'\t\t\t\t\t<Property Name="{n}">\n\t\t\t\t\t\t<Value>\n\t\t\t\t\t\t\t<![CDATA[{v}]]>\n\t\t\t\t\t\t</Value>\n\t\t\t\t\t</Property>\n'
    return ('\t\t\t<Events>\n\t\t\t\t<Event>\n' + ep('ID', event_id) + ep('Name', event_name) + ep('Param', '')
            + ep('Macros', macro) + ep('Conditions', '') + ep('KeyCode', 0) + '\t\t\t\t</Event>\n\t\t\t</Events>\n')

# ================================================================ Dialog-Vorlage
GREEN, WHITE, BLACK, GREY, SHADOW = 39168, 16777215, 0, 12632256, 8421504
NAVY, YELLOW, RED, BLUE = 10027008, 65535, 255, 16711680

# Schriften (DataMask-Bereich 23000-23499)
font(23400, 'FontAttributes_Dlg_8x12_black', 9, 12, 8, 6, BLACK)
font(23401, 'FontAttributes_Dlg_8x12_white', 9, 12, 8, 6, WHITE)
font(23402, 'FontAttributes_Dlg_12x16_white', 12, 16, 12, 9, WHITE)
font(23403, 'FontAttributes_Dlg_12x16_black', 12, 16, 12, 9, BLACK)
# Linien (24000-24499)
line_attr(24400, 'LineAttributes_Dlg_none_white', WHITE, 0)
line_attr(24401, 'LineAttributes_Dlg_Frame', GREEN, 3)
line_attr(24402, 'LineAttributes_Dlg_none_grey', SHADOW, 0)
# Fuellungen (25000-25499)
fill_attr(25400, 'FillAttributes_Dlg_White', WHITE)
fill_attr(25401, 'FillAttributes_Dlg_Shadow', SHADOW)
fill_attr(25402, 'FillAttributes_Dlg_Title', GREEN)
fill_attr(25403, 'FillAttributes_Dlg_Icon_Info', GREEN)
fill_attr(25404, 'FillAttributes_Dlg_Icon_Question', NAVY)
fill_attr(25405, 'FillAttributes_Dlg_Icon_Warning', YELLOW)
fill_attr(25406, 'FillAttributes_Dlg_Icon_Error', RED)

# Maße
MASK_W = MASK_H = 480
BOX_L, BOX_T, BOX_W, BOX_H = 40, 120, 400, 240
IN_W, IN_H = BOX_W - 6, BOX_H - 6
TITLE_H = 36
BTN_W, BTN_H, BTN_GAP = 114, 44, 10
ROW_W = IN_W - 32

# Rechtecke (14000-14499)
rect(14400, 'Rectangle_Dlg_Cover', MASK_W, MASK_H, 25400, 24400)
rect(14401, 'Rectangle_Dlg_Shadow', IN_W, IN_H, 25401, 24402)
rect(14402, 'Rectangle_Dlg_Background', IN_W, IN_H, 25400, 24401)
rect(14403, 'Rectangle_Dlg_Titlebar', IN_W, TITLE_H, 25402, 24402)

# Icons: Ellipse + Zeichen (Ellipse 15000-15499, Text 11000-11499)
icons = [('Info', 'i', 25403, 23402), ('Question', '?', 25404, 23402),
         ('Warning', '!', 25405, 23403), ('Error', 'X', 25406, 23402)]
for n, (name, ch, fill, fnt) in enumerate(icons):
    ellipse(15400 + n, f'Ellipse_Dlg_Icon_{name}', 24, 24, fill, 24402)
    text(11420 + n, f'OutputString_Dlg_Icon_{name}', ch, 24, 24, fnt, align_h=1, align_v=1)
    group(3402 + n, f'Container_Dlg_Icon_{name}', 24, 24,
          [proxy(15400 + n, 0, 0, 'Ellipse'), proxy(11420 + n, 0, 4, 'Text')])

# Titel (Standard-Titel, das Projekt kann eigene Strings nehmen)
titles = ['Hinweis', 'Frage', 'Warnung', 'Fehler']
for n, t in enumerate(titles):
    text(11410 + n, f'OutputString_Dlg_Title_{["Info","Question","Warning","Error"][n]}', t, 340, 16, 23401)

# Buttons: KeyCode = Windows-IDs (IDOK=1 ... IDNO=7)
btns = [(1, 'OK', 'OK'), (2, 'Cancel', 'Abbrechen'), (3, 'Abort', 'Abbrechen'), (4, 'Retry', 'Wiederholen'),
        (5, 'Ignore', 'Ignorieren'), (6, 'Yes', 'Ja'), (7, 'No', 'Nein')]
def row_left(count):
    total = count * BTN_W + (count - 1) * BTN_GAP
    start = (ROW_W - total) // 2
    return [start + i * (BTN_W + BTN_GAP) for i in range(count)]

# 7 Buttons, ID = 6900 + KeyCode - 1; jede Reihe haengt dieselben Buttons per eigenem CProxy ein.
for code, name, label in btns:
    text(11400 + code - 1, f'OutputString_Dlg_Btn_{name}', label, BTN_W - 8, BTN_H - 8, 23400, align_h=1, align_v=1)
    button(6900 + code - 1, f'Button_Dlg_{name}', code, BTN_W, BTN_H, [proxy(11400 + code - 1, 4, 4, 'Text')])
rows = [('OK', ['OK']), ('OKCancel', ['OK', 'Cancel']), ('AbortRetryIgnore', ['Abort', 'Retry', 'Ignore']),
        ('YesNoCancel', ['Yes', 'No', 'Cancel']), ('YesNo', ['Yes', 'No']), ('RetryCancel', ['Retry', 'Cancel'])]
code_of = {name: code for code, name, _ in btns}
for n, (rname, names) in enumerate(rows):
    kids = [proxy(6900 + code_of[b] - 1, x, 0, 'Button') for b, x in zip(names, row_left(len(names)))]
    group(3410 + n, f'Container_Dlg_Buttons_{rname}', ROW_W, BTN_H, kids)

# ObjectPointer (27000er, oberes Ende)
pointer(27900, 'ObjectPointer_Dlg_Cover')
pointer(27901, 'ObjectPointer_Dlg_Icon', proxy(3402, 0, 0, 'Group'))
pointer(27902, 'ObjectPointer_Dlg_Title', proxy(11410, 0, 0, 'Text'))
pointer(27903, 'ObjectPointer_Dlg_Text')
pointer(27904, 'ObjectPointer_Dlg_Buttons')

# Dialog-Box und Gesamt-Container
group(3401, 'Container_Dlg_Box', BOX_W, BOX_H, [
    proxy(14401, 6, 6, 'Rectangle'),
    proxy(14402, 0, 0, 'Rectangle'),
    proxy(14403, 0, 0, 'Rectangle'),
    proxy(27901, 8, 6, 'Pointer'),
    proxy(27902, 40, 10, 'Pointer'),
    proxy(27903, 16, TITLE_H + 14, 'Pointer'),
    proxy(27904, 16, IN_H - BTN_H - 12, 'Pointer'),
])
group(3400, 'Container_Dialog', MASK_W, MASK_H, [
    proxy(27900, 0, 0, 'Pointer'),
    proxy(3401, BOX_L, BOX_T, 'Group'),
], hidden=1)

# ================================================================ Übungsobjekte
font(23001, 'FontAttributes_8x12', 9, 12, 8, 6, BLACK)
examples = [
    (11020, 'OutputString_Text_Toast', 'Dies ist ein Toast. Er verschwindet nach 3 s von selbst.'),
    (11021, 'OutputString_Text_OK', 'Aufnahme nicht gestartet: Zapfwelle läuft nicht. Bitte zuerst Zapfwelle einschalten.'),
    (11022, 'OutputString_Text_Frage', 'Einstellungen speichern?'),
]
for jid, oname, s in examples:
    text(jid, oname, s, ROW_W, 110, 23400)

text(11014, 'OutputString_Result', 'RESULT:', 80, 20, 23001)
output_number(12000, 'OutputNumber_Result', 60, 20, 23001)
text(11015, 'OutputString_DataMask_M2', 'DataMask_M2', 110, 20, 23000)
for n, lbl in enumerate(['Test 1', 'Test 2', 'Test 3']):
    text(11016 + n, f'OutputString_Button_Test{n + 1}', lbl, 152, 52, 23001, align_h=1, align_v=1)
    button(6000 + n, f'Button_Test{n + 1}', 10 + n, 160, 60, [proxy(11016 + n, 4, 4, 'Text')])

# Softkeys F2..F6 (Text im SoftKeyMask-Bereich 11500ff)
sks = [(5001, 'SoftKey_F2', 2, 'OK', ''), (5002, 'SoftKey_F3', 3, 'OK modal', ''),
       (5003, 'SoftKey_F4', 4, 'Ja Nein Abbr.', ''), (5004, 'SoftKey_F5', 5, 'Maske 1', '1'),
       (5005, 'SoftKey_F6', 6, 'Maske 2', '2')]
for jid, oname, kc, lbl, mac in sks:
    tid = 11500 + jid - 5000
    text(tid, f'OutputString_{oname}', lbl, 80, 20, 23000, transparent=0)
    softkey(jid, oname, kc, [proxy(tid, 0, 30, 'Text')], macro_event(24, 'OnKeyPress', mac) if mac else '')

# Makros: Maskenwechsel
for mid, mask_id, mask_name in [(1, 1000, 'DataMask_M1'), (2, 1001, 'DataMask_M2')]:
    out.append(f'\t\t<Object Class="CMacro" JVS-ID="{mid}" ObjectName="Macro_{mask_name}" Pinned="FALSE">\n'
               '\t\t\t<Commands>\n\t\t\t\t<Command id="173" subid="-1">\n\t\t\t\t\t<Params>\n'
               '\t\t\t\t\t\t<Param Name="Workingset" Type="7">0 - WorkingSet</Param>\n'
               f'\t\t\t\t\t\t<Param Name="New active Mask" Type="8">{mask_id} - {mask_name}</Param>\n'
               '\t\t\t\t\t</Params>\n\t\t\t\t</Command>\n\t\t\t</Commands>\n'
               + prop('Comment', 'AAA=', True).replace('\t\t\t\t<P', '\t\t\t<P') + '\t\t</Object>\n')

out.append('\t\t<Object Class="CDataMask" Name="" ObjectName="DataMask_Dlg_Vorlagen_invisible" Pinned="FALSE" JVS-ID="1002" JVS-RefCount="1">\n'
           '\t\t\t<PropertySheet Name="Model">\n' + prop('MaskType', 1) + prop('Path', '.\\DataMask_Dlg_Vorlagen_invisible.jvi')
           + prop('Comment', 'AAA=', True) + '\t\t\t</PropertySheet>\n\t\t</Object>\n')
# DataMask_M2 im .jop
out.append('\t\t<Object Class="CDataMask" Name="" ObjectName="DataMask_M2" Pinned="FALSE" JVS-ID="1001" JVS-RefCount="1">\n'
           '\t\t\t<PropertySheet Name="Model">\n' + prop('MaskType', 1) + prop('Path', '.\\DataMask_M2.jvi')
           + prop('Comment', 'AAA=', True) + '\t\t\t</PropertySheet>\n\t\t</Object>\n')


# Softkey F1 -> "Toast"
f1 = re.search(r'(ObjectName="OutputString_SoftKey_F1".*?</Object>)', jop, re.S).group(1)
f1n = f1.replace(enc('SoftKey_F1'), enc('Toast'))
jop = jop.replace(f1, f1n)

end = '\t</Objects>\n</JetView-ObjectPool>'
assert end in jop
jop = jop.replace(end, ''.join(out) + end)
jop_p.write_text(jop, encoding='utf-8', newline='\n')

# ================================================================ .jvi
def component(cls, name, jid, left, top, z, extra=''):
    cid = random.randint(10_000_000, 600_000_000)
    return (f'\t\t<Component ID="{cid}" Class="{cls}" Name="{name}">\n\t\t\t<PropertySheets>\n'
            f'\t\t\t\t<PropertySheet Name="General">\n\t\t\t\t\t<Property Name="ZOrder">\n\t\t\t\t\t\t<Value>{z}</Value>\n'
            '\t\t\t\t\t</Property>\n\t\t\t\t</PropertySheet>\n\t\t\t\t<PropertySheet Name="Proxy">\n'
            f'\t\t\t\t\t<Property Name="Top">\n\t\t\t\t\t\t<Value>{top}</Value>\n\t\t\t\t\t</Property>\n'
            f'\t\t\t\t\t<Property Name="Left">\n\t\t\t\t\t\t<Value>{left}</Value>\n\t\t\t\t\t</Property>\n'
            '\t\t\t\t\t<Property Name="Transform">\n'
            f'\t\t\t\t\t\t<Value>(1.0000000000000000)(0.0000000000000000)({left:.16f})(0.0000000000000000)(1.0000000000000000)({top:.16f})</Value>\n'
            '\t\t\t\t\t</Property>\n\t\t\t\t\t<Property Name="ReferencedObjectForMask">\n\t\t\t\t\t\t<Value>-1</Value>\n'
            f'\t\t\t\t\t</Property>\n{extra}\t\t\t\t</PropertySheet>\n\t\t\t</PropertySheets>\n\t\t\t<Objects>\n'
            f'\t\t\t\t<Object JVS-ID="{jid}"/>\n\t\t\t</Objects>\n\t\t</Component>\n')

def add_components(path, comps):
    t = path.read_text(encoding='utf-8')
    t = t.replace('\t</Components>', ''.join(comps) + '\t</Components>')
    path.write_text(t, encoding='utf-8', newline='\n')

def test_widgets(start_z, buttons):
    c = []
    z = start_z
    for n, (bid, left, top) in enumerate(buttons):
        c.append(component('CButton', 'Button', bid, left, top, z)); z += 1
    c.append(component('COutputText', 'Text', 11014, 20, 420, z)); z += 1
    c.append(component('COutputNumber', 'Text', 12000, 100, 420, z)); z += 1
    c.append(component('CGroup', 'Group', 3400, 0, 0, z))   # Dialog immer zuletzt = oben
    return c

m1 = pool / 'DataMask_M1.jvi'
add_components(m1, test_widgets(1, [(6000, 40, 160), (6001, 280, 160)]))

m2 = pool / 'DataMask_M2.jvi'
t = m1.read_text(encoding='utf-8')
t = t.replace('<Value>1000</Value>', '<Value>1001</Value>', 1)
t = re.sub(r'\t\t<Component .*?</Component>\n', '', t, flags=re.S)
m2.write_text(t, encoding='utf-8', newline='\n')
add_components(m2, [component('COutputText', 'Text', 11015, 370, 460, 0)]
               + test_widgets(1, [(6002, 160, 200)]))

vm = pool / 'DataMask_Dlg_Vorlagen_invisible.jvi'
t = m1.read_text(encoding='utf-8')
t = t.replace('<Value>1000</Value>', '<Value>1002</Value>', 1)
t = re.sub(r'\t\t<Component .*?</Component>\n', '', t, flags=re.S)
vm.write_text(t, encoding='utf-8', newline='\n')
vc = []
z = 0
vc.append(component('CRectangle', 'Rectangle', 14400, 0, 0, z)); z += 1
for n in range(4):
    vc.append(component('CGroup', 'Group', 3402 + n, 10 + 30 * n, 10, z)); z += 1
    vc.append(component('COutputText', 'Text', 11410 + n, 10, 40 + 20 * n, z)); z += 1
for n in range(6):
    vc.append(component('CGroup', 'Group', 3410 + n, 10, 130 + 50 * n, z)); z += 1
for n, jid in enumerate([11020, 11021, 11022]):
    vc.append(component('COutputText', 'Text', jid, 380 if n else 10, 10 + 120 * n if n else 440, z)); z += 1
add_components(vm, vc)

skm = pool / 'SoftKeyMask_S1.jvi'
add_components(skm, [component('CSoftKey', 'SoftKey', jid, 560, 80 * n, 0,
                               '\t\t\t\t\t<Property Name="SoftkeymaskDesignatorNo">\n'
                               f'\t\t\t\t\t\t<Value>{n}</Value>\n\t\t\t\t\t</Property>\n')
                     for n, jid in enumerate([5001, 5002, 5003, 5004, 5005], start=1)])
print('ok, proxies bis', next_proxy - 1)
