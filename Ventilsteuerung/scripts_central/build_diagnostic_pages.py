"""Generate the Ausgaenge/Eingaenge diagnostic scroll pages into DefaultPool.jop.

Reads combined_APIXON_Pin_Zuordnung.csv for the Q/I channel rows and a hardcoded
list of Bosch MM7.10 IMU fields for the extra Eingaenge section, then appends all
new pool objects (2 DataMasks, 2 SoftKeyMasks, scroll containers, data/header
rows, shared background/status objects) as raw text to DefaultPool.jop, preserving
CRLF line endings. See AUSGAENGE_EINGAENGE_POOL_PLAN.md for the design.

Structure only - no live-value wiring, no macros/navigation (added by hand),
no FB-side ScrollFS_PHYS wiring (separate next step).
"""
import argparse
import base64
import csv
import io
import os
import re
from collections import OrderedDict

_parser = argparse.ArgumentParser(description=__doc__)
_parser.add_argument(
    "-d", "--pool-dir", dest="pool_dir", required=True,
    help="ISO-Designer pool workspace folder, relative to this script's "
         "parent directory (i.e. relative to the project's Ventilsteuerung/ "
         "folder) - e.g. ISO-DesignerProjects/Workspace/DefaultPool",
)
_parser.add_argument(
    "-c", "--csv", dest="csv_path", required=True,
    help="Path to combined_APIXON_Pin_Zuordnung.csv (not committed to the "
         "repo - supply the actual location, e.g. on a shared drive)",
)
_args, _ = _parser.parse_known_args()
_script_dir = os.path.dirname(os.path.abspath(__file__))
JOP_PATH = os.path.join(os.path.dirname(_script_dir), _args.pool_dir, "DefaultPool.jop")
JOP_DIR = os.path.dirname(JOP_PATH)
CSV_PATH = _args.csv_path

ROW_HEIGHT = 42
ROW_H = 36  # row container's own Height (leaves a visible gap, matching Workspace_Scroll)
ROW_W = 432
HEADER_H = 36
LIST_PARENT_W = 480
LIST_PARENT_H = 288
BAR_PARENT_W = 12
BAR_PARENT_H = 288
BAR_PARENT_LEFT = 458
BAR_THUMB_H = 36
MASK_W = 480
MASK_H = 480

# COLORREF-style decimal (R + G*256 + B*65536), matching the convention already
# validated in Workspace_Scroll's zebra-stripe FillAttributes_RowAlt (0xE6E6E6).
COLOR_STATUS_GREY = 12632256   # 0xC0C0C0 - inactive/no data yet
COLOR_STATUS_GREEN = 49152     # 0x00C000 - OK
COLOR_STATUS_RED = 192         # 0x0000C0-ish red channel only -> R=192,G=0,B=0
COLOR_ROW_BG = 15132390        # 0xE6E6E6, same as Workspace_Scroll's Rectangle_RowAlt
COLOR_HEADER_BG = 12632256     # 0xC0C0C0 - clearly darker than the plain white/E6E6E6 rows
COLOR_BORDER = 11184810        # 0xAAAAAA

BOSCH_FIELDS = [
    ("rAccX", "Beschleunigung X [m/s^2]"),
    ("rAccY", "Beschleunigung Y [m/s^2]"),
    ("rAccZ", "Beschleunigung Z [m/s^2]"),
    ("rRateX", "Drehrate X [deg/s]"),
    ("rRateY", "Drehrate Y [deg/s]"),
    ("rRateZ", "Drehrate Z [deg/s]"),
    ("rRoll", "Neigung Roll [deg]"),
    ("rPitch", "Neigung Pitch [deg]"),
    ("rYaw", "Neigung Yaw [deg]"),
    ("rTempRateZ", "Sensortemperatur [degC]"),
    ("uiHW_Index", "HW-Index (0=MM5.10, 1=MM7.10)"),
    ("eStatusAccX", "Status AccX"),
    ("eStatusAccY", "Status AccY"),
    ("eStatusAccZ", "Status AccZ"),
    ("eStatusRateX", "Status RateX"),
    ("eStatusRateY", "Status RateY"),
    ("eStatusRateZ", "Status RateZ"),
    ("bAllSignalsReady", "Alle Signale bereit"),
    ("uiSysStatus", "Systemstatus (TX1)"),
    ("uiSysStatus5", "Systemstatus (TX2)"),
    ("uiSysDiag", "Diagnosecode (TX2)"),
    ("uiMessageCounter", "Nachrichtenzaehler"),
    ("bCommError", "CAN-Timeout"),
    ("bCRCError", "CRC-Fehler"),
]


def encode_text(s):
    """UTF-16LE + null terminator + base64, matching ISO-Designer's text property encoding."""
    return base64.b64encode((s + "\0").encode("utf-16-le")).decode("ascii")


# ISO 11783-6 Annex B object-ID blocks (see GENERATIVER_POOL_PLAN.md Abschnitt 3).
# JVS-ID is the same numbering as the wire-protocol ObjectID, not a separate
# internal-only counter - a class with zero existing objects must still start
# at its block's floor, never at 0 (0 is CWorkingSet's own reserved ID).
CLASS_ID_FLOOR = {
    "CDataMask": 999,
    "CAlarmMask": 1999,
    "CGroup": 2999,          # Container
    "CSoftKeyMask": 3999,
    "CSoftKey": 4999,
    "CButton": 5999,
    "CInputBoolean": 6999,
    "CInputString": 7999,
    "CInputNumber": 8999,
    "CInputList": 9999,
    "COutputText": 10999,    # OutputString
    "COutputNumber": 11999,
    "CLine": 12999,
    "CRectangle": 13999,
    "CEllipse": 14999,
    "CPolygon": 15999,
    "CMeter": 16999,
    "CLinearBarGraph": 17999,
    "CArchedBarGraph": 18999,
    "CImage": 19999,         # PictureGraphic
    "CNumberVariable": 20999,
    "CStringVariable": 21999,
    "CFontStyle": 22999,     # FontAttributes
    "CLineStyle": 23999,     # LineAttributes
    "CFillStyle": 24999,     # FillAttributes
    "CInputAttributes": 25999,
    "CPointer": 26999,       # ObjectPointer
}


class IdAllocator:
    def __init__(self, jop_text):
        self.max_ids = dict(CLASS_ID_FLOOR)
        for m in re.finditer(r'Class="(C\w+)"[^>]*?JVS-ID="(\d+)"', jop_text):
            cls, jid = m.group(1), int(m.group(2))
            if jid < 60000:  # ignore CProxy's own huge ID space here, handled separately
                self.max_ids[cls] = max(self.max_ids.get(cls, -1), jid)
        proxy_ids = [int(m) for m in re.findall(r'Class="CProxy"[^>]*?JVS-ID="(\d+)"', jop_text)]
        self.max_ids["CProxy"] = max(proxy_ids) if proxy_ids else 4194303

    def next_id(self, cls):
        if cls not in self.max_ids and cls not in CLASS_ID_FLOOR:
            raise KeyError(f"no ISO 11783-6 ID-block floor known for class {cls!r} - add it to CLASS_ID_FLOOR")
        self.max_ids[cls] = self.max_ids.get(cls, -1) + 1
        return self.max_ids[cls]


def load_csv_rows():
    with open(CSV_PATH, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    groups = OrderedDict()
    for r in rows:
        key = (int(r["Modul_Nr"]), r["Pin"])
        groups.setdefault(key, []).append(r)

    def build(prefix):
        out = OrderedDict()
        for (modul, pin), items in groups.items():
            if not pin.startswith(prefix):
                continue
            refs = []
            names = []
            for it in items:
                ref = (it.get("Ziel_Ref") or "").strip()
                name = (it.get("Ziel_Bezeichnung") or "").strip()
                if ref and ref not in refs:
                    refs.append(ref)
                if name and name not in names:
                    names.append(name)
            out.setdefault(modul, []).append({
                "pin": pin,
                "anschluss": ", ".join(refs),
                "funktion": ", ".join(names),
            })
        return out

    return build("Q"), build("I")


def pin_sort_key(entry):
    m = re.search(r"(\d+)", entry["pin"])
    return int(m.group(1)) if m else 0


# ---------------------------------------------------------------------------
# Object emitters (2-tab base indent, matching DefaultPool.jop's top-level <Object> convention)
# ---------------------------------------------------------------------------

def emit_group(jid, object_name, width, height, clips=1):
    return (
        f'\t\t<Object Class="CGroup" Name="{object_name}" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}">\n'
        f'\t\t\t<PropertySheet Name="Group">\n'
        f'\t\t\t\t<Property Name="Hidden">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ClipsChildren">\n\t\t\t\t\t<Value>{clips}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Width">\n\t\t\t\t\t<Value>{width}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Height">\n\t\t\t\t\t<Value>{height}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Visible">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Locked">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Disabled">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t\t<Objects>\n{{CHILDREN}}\t\t\t</Objects>\n'
        f'\t\t</Object>\n'
    )


def emit_group_with_children(jid, object_name, width, height, child_ids, clips=1):
    tpl = emit_group(jid, object_name, width, height, clips)
    children = "".join(f'\t\t\t\t<Object JVS-ID="{c}"/>\n' for c in child_ids)
    return tpl.replace("{CHILDREN}", children)


def emit_output_string(jid, object_name, text, width=140, height=18):
    encoded = encode_text(text)
    return (
        f'\t\t<Object Class="COutputText" Name="{object_name}" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}">\n'
        f'\t\t\t<PropertySheet Name="Text">\n'
        f'\t\t\t\t<Property Name="Text">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[{encoded}]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ResourceID">\n\t\t\t\t\t<Value/>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="MultiLine">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="WordBreak">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="WrapOnHyphen">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="AlignH">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="AlignV">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Appearance">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ControlType">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Numeric">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Offset">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Scale">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FormatType">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FormatString">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="NoOfDecimals">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Value">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[{encoded}]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="SetLengthAsMaximumLength">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="StringLength">\n\t\t\t\t\t<Value>{max(1, len(text))}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Transparent">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="LeadingZeros">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ZeroAsBlank">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Truncate">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="BkColor">\n\t\t\t\t\t<Value>16777215</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="RoundEdgeRadius">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Width">\n\t\t\t\t\t<Value>{width}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Height">\n\t\t\t\t\t<Value>{height}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Visible">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Locked">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Disabled">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t\t<Objects>\n\t\t\t\t<Object JVS-ID="23000"/>\n\t\t\t</Objects>\n'
        f'\t\t</Object>\n'
    )


def emit_rectangle(jid, object_name, width, height, fill_id, line_id):
    return (
        f'\t\t<Object Class="CRectangle" Name="{object_name}" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}">\n'
        f'\t\t\t<PropertySheet Name="Rectangle">\n'
        f'\t\t\t\t<Property Name="LineSupression">\n\t\t\t\t\t<Value>0000</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="RoundEdgeRadius">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Points">\n\t\t\t\t\t<Value>(0,0)({width},0)({width},{height})(0,{height})</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="OriginalPoints">\n\t\t\t\t\t<Value>(0,0)({width},0)({width},{height})(0,{height})</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Width">\n\t\t\t\t\t<Value>{width}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Height">\n\t\t\t\t\t<Value>{height}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Visible">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Locked">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Disabled">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t\t<Objects>\n\t\t\t\t<Object JVS-ID="{fill_id}"/>\n\t\t\t\t<Object JVS-ID="{line_id}"/>\n\t\t\t</Objects>\n'
        f'\t\t</Object>\n'
    )


def emit_fill_style(jid, object_name, color, transparent=0):
    return (
        f'\t\t<Object Class="CFillStyle" JVS-ID="{jid}" ObjectName="{object_name}" Pinned="FALSE">\n'
        f'\t\t\t<PropertySheet Name="FillStyle" Version="2" ID="68716">\n'
        f'\t\t\t\t<Property Name="HatchStyle">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FillStyle">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="BackColor">\n\t\t\t\t\t<Value>{color}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="ForeColor">\n\t\t\t\t\t<Value>{color}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="TransparentBackground">\n\t\t\t\t\t<Value>{transparent}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FillTransparent">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FillType">\n\t\t\t\t\t<Value>2</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="FillPatternObjectID">\n\t\t\t\t\t<Value>-1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="GradientDirection">\n\t\t\t\t\t<Value>0.000000</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="RadialRefPointIsCenter">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="DistanceInPercentFromStart">\n\t\t\t\t\t<Value>0.000000</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t</Object>\n'
    )


def emit_line_style(jid, object_name, color):
    return (
        f'\t\t<Object Class="CLineStyle" JVS-ID="{jid}" ObjectName="{object_name}" Pinned="FALSE">\n'
        f'\t\t\t<PropertySheet Name="LineStyle">\n'
        f'\t\t\t\t<Property Name="LineWidth">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="LineArt">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="LineColor">\n\t\t\t\t\t<Value>{color}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t</Object>\n'
    )


def emit_proxy(jid, name, target_id, top=0, left=0):
    return (
        f'\t\t<Object Class="CProxy" Name="{name}" ObjectName="" Pinned="FALSE" JVS-ID="{jid}">\n'
        f'\t\t\t<PropertySheet Name="Proxy">\n'
        f'\t\t\t\t<Property Name="Top">\n\t\t\t\t\t<Value>{top}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Left">\n\t\t\t\t\t<Value>{left}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Name">\n\t\t\t\t\t<Value>{name}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="TabIndex">\n\t\t\t\t\t<Value>-1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Transform">\n\t\t\t\t\t<Value>(1.0000000000000000)(0.0000000000000000)({left}.0000000000000000)(0.0000000000000000)(1.0000000000000000)({top}.0000000000000000)</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t\t<Objects>\n\t\t\t\t<Object JVS-ID="{target_id}"/>\n\t\t\t</Objects>\n'
        f'\t\t</Object>\n'
    )


def emit_object_pointer(jid, object_name, target_proxy_id):
    return (
        f'\t\t<Object Class="CPointer" Name="Pointer" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}">\n'
        f'\t\t\t<PropertySheet Name="Pointer">\n'
        f'\t\t\t\t<Property Name="Visible">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Locked">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Disabled">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t\t<Objects>\n\t\t\t\t<Object JVS-ID="{target_proxy_id}"/>\n\t\t\t</Objects>\n'
        f'\t\t</Object>\n'
    )


def emit_softkey(jid, object_name, icon_proxy_id):
    return (
        f'\t\t<Object Class="CSoftKey" Name="SoftKey" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}">\n'
        f'\t\t\t<PropertySheet Name="SoftKey">\n'
        f'\t\t\t\t<Property Name="BackColor">\n\t\t\t\t\t<Value>13421772</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="KeyCode">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Hotkey">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Width">\n\t\t\t\t\t<Value>80</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Height">\n\t\t\t\t\t<Value>80</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Visible">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Disabled">\n\t\t\t\t\t<Value>0</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t\t<Objects>\n\t\t\t\t<Object JVS-ID="{icon_proxy_id}"/>\n\t\t\t</Objects>\n'
        f'\t\t</Object>\n'
    )


def emit_datamask_stub(jid, object_name, path):
    return (
        f'\t\t<Object Class="CDataMask" Name="" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}" JVS-RefCount="1">\n'
        f'\t\t\t<PropertySheet Name="Model">\n'
        f'\t\t\t\t<Property Name="MaskType">\n\t\t\t\t\t<Value>1</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Path">\n\t\t\t\t\t<Value>{path}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t</Object>\n'
    )


def emit_softkeymask_stub(jid, object_name, path):
    return (
        f'\t\t<Object Class="CSoftKeyMask" Name="" ObjectName="{object_name}" Pinned="FALSE" JVS-ID="{jid}" JVS-RefCount="1">\n'
        f'\t\t\t<PropertySheet Name="Model">\n'
        f'\t\t\t\t<Property Name="MaskType">\n\t\t\t\t\t<Value>2</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Path">\n\t\t\t\t\t<Value>{path}</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t\t<Property Name="Comment">\n\t\t\t\t\t<Value>\n\t\t\t\t\t\t<![CDATA[AAA=]]>\n\t\t\t\t\t</Value>\n\t\t\t\t</Property>\n'
        f'\t\t\t</PropertySheet>\n'
        f'\t\t</Object>\n'
    )


_comp_id_counter = [100000000]


def next_comp_id():
    _comp_id_counter[0] += 37
    return _comp_id_counter[0]


def emit_mask_component(cls, name, target_jvs_id, top, left, softkey_designator=None):
    extra = ""
    if softkey_designator is not None:
        extra = (
            f'\t\t\t\t\t<Property Name="SoftkeymaskDesignatorNo">\n'
            f'\t\t\t\t\t\t<Value>{softkey_designator}</Value>\n\t\t\t\t\t</Property>\n'
        )
    return (
        f'\t\t<Component ID="{next_comp_id()}" Class="{cls}" Name="{name}">\n'
        f'\t\t\t<PropertySheets>\n'
        f'\t\t\t\t<PropertySheet Name="General">\n'
        f'\t\t\t\t\t<Property Name="ZOrder">\n\t\t\t\t\t\t<Value>0</Value>\n\t\t\t\t\t</Property>\n'
        f'\t\t\t\t</PropertySheet>\n'
        f'\t\t\t\t<PropertySheet Name="Proxy">\n'
        f'\t\t\t\t\t<Property Name="Top">\n\t\t\t\t\t\t<Value>{top}</Value>\n\t\t\t\t\t</Property>\n'
        f'\t\t\t\t\t<Property Name="Left">\n\t\t\t\t\t\t<Value>{left}</Value>\n\t\t\t\t\t</Property>\n'
        f'\t\t\t\t\t<Property Name="Transform">\n'
        f'\t\t\t\t\t\t<Value>(1.0000000000000000)(0.0000000000000000)({left}.0000000000000000)(0.0000000000000000)(1.0000000000000000)({top}.0000000000000000)</Value>\n'
        f'\t\t\t\t\t</Property>\n'
        f'\t\t\t\t\t<Property Name="ReferencedObjectForMask">\n\t\t\t\t\t\t<Value>-1</Value>\n\t\t\t\t\t</Property>\n'
        f'{extra}'
        f'\t\t\t\t</PropertySheet>\n'
        f'\t\t\t</PropertySheets>\n'
        f'\t\t\t<Objects>\n\t\t\t\t<Object JVS-ID="{target_jvs_id}"/>\n\t\t\t</Objects>\n'
        f'\t\t</Component>\n'
    )


def emit_datamask_jvi(object_id, softkeymask_id, components_xml):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<JetView-Document Version="0" ObjectPoolVersion="3.0" ProductVersion="5.7.2.6664">\r\n'
        '\t<PropertySheets>\r\n'
        '\t\t<PropertySheet Name="General">\r\n'
        f'\t\t\t<Property Name="ObjectID">\r\n\t\t\t\t<Value>{object_id}</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Titel">\r\n\t\t\t\t<Value>\r\n\t\t\t\t\t<![CDATA[]]>\r\n\t\t\t\t</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="BackColor">\r\n\t\t\t\t<Value>16777215</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="MaskType">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="RelatedObjectPool">\r\n\t\t\t\t<Value>.\\DefaultPool.jop</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="AlarmPriority">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="AcusticSignal">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Available">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Transparent">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="CellFormat">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="WindowType">\r\n\t\t\t\t<Value>0</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="WindowNameObjectID">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="KeyGroupNameObjectID">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="WindowTitleObjectID">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="WindowIconObjectID">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="WindowRefObjectID1">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="WindowRefObjectID2">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        f'\t\t\t<Property Name="SoftKeyMask">\r\n\t\t\t\t<Value>{softkeymask_id}</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Selectable">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="ActiveMask">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="ActiveMaskExtended">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Languages">\r\n\t\t\t\t<Value>en;de</Value>\r\n\t\t\t</Property>\r\n'
        f'\t\t\t<Property Name="Width">\r\n\t\t\t\t<Value>{MASK_W}</Value>\r\n\t\t\t</Property>\r\n'
        f'\t\t\t<Property Name="Height">\r\n\t\t\t\t<Value>{MASK_H}</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="DisplayType">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="ScalingAspectRatioMode">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="EnableScrolling">\r\n\t\t\t\t<Value>0</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t</PropertySheet>\r\n'
        '\t\t<PropertySheet Name="Image">\r\n'
        '\t\t\t<Property Name="ObjectID">\r\n\t\t\t\t<Value>-1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t</PropertySheet>\r\n'
        '\t\t<PropertySheet Name="Layout">\r\n'
        '\t\t\t<Property Name="GridVisible">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="SnapToGrid">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="AngleSnap">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="RulerVisible">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="VerticalSpacing">\r\n\t\t\t\t<Value>10</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="HorizontalSpacing">\r\n\t\t\t\t<Value>10</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="GridColor">\r\n\t\t\t\t<Value>8421504</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="MagnificationX">\r\n\t\t\t\t<Value>175</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="MagnificationY">\r\n\t\t\t\t<Value>175</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t</PropertySheet>\r\n'
        '\t</PropertySheets>\r\n'
        '\t<Components>\r\n'
        f'{components_xml}'
        '\t</Components>\r\n'
        '</JetView-Document>\r\n'
    )


def emit_softkeymask_jvi(object_id, components_xml):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        '<JetView-Document Version="0" ObjectPoolVersion="3.0" ProductVersion="5.7.2.6664">\r\n'
        '\t<PropertySheets>\r\n'
        '\t\t<PropertySheet Name="General">\r\n'
        f'\t\t\t<Property Name="ObjectID">\r\n\t\t\t\t<Value>{object_id}</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Titel">\r\n\t\t\t\t<Value>\r\n\t\t\t\t\t<![CDATA[]]>\r\n\t\t\t\t</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="BackColor">\r\n\t\t\t\t<Value>13421772</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="MaskType">\r\n\t\t\t\t<Value>2</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="RelatedObjectPool">\r\n\t\t\t\t<Value>.\\DefaultPool.jop</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Available">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Languages">\r\n\t\t\t\t<Value>en;de</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Width">\r\n\t\t\t\t<Value>640</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="Height">\r\n\t\t\t\t<Value>480</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="DisplayType">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t</PropertySheet>\r\n'
        '\t\t<PropertySheet Name="Layout">\r\n'
        '\t\t\t<Property Name="GridVisible">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t\t<Property Name="SnapToGrid">\r\n\t\t\t\t<Value>1</Value>\r\n\t\t\t</Property>\r\n'
        '\t\t</PropertySheet>\r\n'
        '\t</PropertySheets>\r\n'
        '\t<Components>\r\n'
        f'{components_xml}'
        '\t</Components>\r\n'
        '</JetView-Document>\r\n'
    )


# ---------------------------------------------------------------------------
# Shared objects (built once, used by both pages)
# ---------------------------------------------------------------------------

class Shared:
    pass


def build_shared_objects(alloc, out):
    s = Shared()

    row_fill = alloc.next_id("CFillStyle")
    row_line = alloc.next_id("CLineStyle")
    out.append(emit_fill_style(row_fill, "FillAttributes_RowBg", COLOR_ROW_BG, transparent=0))
    out.append(emit_line_style(row_line, "LineAttributes_RowBorder", COLOR_BORDER))
    s.row_bg_rect = alloc.next_id("CRectangle")
    out.append(emit_rectangle(s.row_bg_rect, "Rectangle_RowBg", ROW_W, ROW_H, row_fill, row_line))

    header_fill = alloc.next_id("CFillStyle")
    out.append(emit_fill_style(header_fill, "FillAttributes_HeaderBg", COLOR_HEADER_BG, transparent=0))
    s.header_bg_rect = alloc.next_id("CRectangle")
    out.append(emit_rectangle(s.header_bg_rect, "Rectangle_HeaderBg", ROW_W, HEADER_H, header_fill, row_line))

    grey_fill = alloc.next_id("CFillStyle")
    green_fill = alloc.next_id("CFillStyle")
    red_fill = alloc.next_id("CFillStyle")
    out.append(emit_fill_style(grey_fill, "FillAttributes_StatusGrey", COLOR_STATUS_GREY, transparent=0))
    out.append(emit_fill_style(green_fill, "FillAttributes_StatusGreen", COLOR_STATUS_GREEN, transparent=0))
    out.append(emit_fill_style(red_fill, "FillAttributes_StatusRed", COLOR_STATUS_RED, transparent=0))
    s.status_grey_rect = alloc.next_id("CRectangle")
    s.status_green_rect = alloc.next_id("CRectangle")
    s.status_red_rect = alloc.next_id("CRectangle")
    out.append(emit_rectangle(s.status_grey_rect, "Rectangle_StatusGrey", 18, 18, grey_fill, row_line))
    out.append(emit_rectangle(s.status_green_rect, "Rectangle_StatusGreen", 18, 18, green_fill, row_line))
    out.append(emit_rectangle(s.status_red_rect, "Rectangle_StatusRed", 18, 18, red_fill, row_line))

    bar_fill = alloc.next_id("CFillStyle")
    thumb_fill = alloc.next_id("CFillStyle")
    out.append(emit_fill_style(bar_fill, "FillAttributes_BarTrack", COLOR_BORDER, transparent=0))
    out.append(emit_fill_style(thumb_fill, "FillAttributes_BarThumb", COLOR_STATUS_GREY, transparent=0))
    s.bar_track_rect = alloc.next_id("CRectangle")
    s.bar_thumb_rect = alloc.next_id("CRectangle")
    out.append(emit_rectangle(s.bar_track_rect, "Rectangle_BarTrack", BAR_PARENT_W, BAR_PARENT_H, bar_fill, row_line))
    out.append(emit_rectangle(s.bar_thumb_rect, "Rectangle_BarThumb", BAR_PARENT_W, BAR_THUMB_H, thumb_fill, row_line))

    return s


# ---------------------------------------------------------------------------
# Row builders
# ---------------------------------------------------------------------------

def build_data_row(alloc, out, shared, top, col1, col2, col3, prefix, row_number):
    id_col1 = alloc.next_id("COutputText")
    id_col2 = alloc.next_id("COutputText")
    id_col3 = alloc.next_id("COutputText")
    out.append(emit_output_string(id_col1, f"OutputString_{id_col1}", col1, width=110))
    out.append(emit_output_string(id_col2, f"OutputString_{id_col2}", col2, width=180))
    out.append(emit_output_string(id_col3, f"OutputString_{id_col3}", col3, width=100))

    status_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(status_proxy, "StatusColor", shared.status_grey_rect, 0, 0))
    ptr_id = alloc.next_id("CPointer")
    out.append(emit_object_pointer(ptr_id, f"ObjectPointer_Status_{ptr_id}", status_proxy))

    bg_proxy = alloc.next_id("CProxy")
    c1_proxy = alloc.next_id("CProxy")
    c2_proxy = alloc.next_id("CProxy")
    c3_proxy = alloc.next_id("CProxy")
    ptr_wrap_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(bg_proxy, "RowBg", shared.row_bg_rect, 0, 0))
    out.append(emit_proxy(c1_proxy, f"OutputString_{id_col1}", id_col1, 2, 4))
    out.append(emit_proxy(c2_proxy, f"OutputString_{id_col2}", id_col2, 2, 118))
    out.append(emit_proxy(c3_proxy, f"OutputString_{id_col3}", id_col3, 2, 302))
    out.append(emit_proxy(ptr_wrap_proxy, f"ObjectPointer_Status_{ptr_id}", ptr_id, 9, 408))

    # "_Row_01"/"_Row_02" naming (sequential across the whole page, headers don't
    # consume a number) is required by GcfScript.py's readScrollJOP(): it derives
    # row_height from the Top-spacing between whichever containers are named
    # "*_Row_01" and "*_Row_02". Since headers advance `top` by the same
    # ROW_HEIGHT as data rows (see build_page), any two consecutively-numbered
    # data rows are exactly ROW_HEIGHT apart, header or not in between doesn't
    # matter for rows 01/02 specifically since nothing sits between a module's
    # own first two rows.
    row_name = f"{prefix}_Row_{row_number:02d}"
    container_id = alloc.next_id("CGroup")
    out.append(emit_group_with_children(
        container_id, row_name, ROW_W, ROW_H,
        [bg_proxy, c1_proxy, c2_proxy, c3_proxy, ptr_wrap_proxy]))

    embed_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(embed_proxy, row_name, container_id, top, 0))
    return embed_proxy


def build_header_row(alloc, out, shared, top, title):
    id_title = alloc.next_id("COutputText")
    out.append(emit_output_string(id_title, f"OutputString_{id_title}", title, width=300))

    bg_proxy = alloc.next_id("CProxy")
    title_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(bg_proxy, "HeaderBg", shared.header_bg_rect, 0, 0))
    out.append(emit_proxy(title_proxy, f"OutputString_{id_title}", id_title, 8, 8))

    container_id = alloc.next_id("CGroup")
    out.append(emit_group_with_children(
        container_id, f"Container_Header_{container_id}", ROW_W, HEADER_H,
        [bg_proxy, title_proxy]))

    embed_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(embed_proxy, f"Container_Header_{container_id}", container_id, top, 0))
    return embed_proxy


# ---------------------------------------------------------------------------
# Page (DataMask + SoftKeyMask) builder
# ---------------------------------------------------------------------------

SOFTKEY_SPEC = [
    ("FIRST", "SoftKey_FIRST"),
    ("PAGE_UP", "SoftKey_PAGE_UP"),
    ("UP", "SoftKey_UP"),
    ("DOWN", "SoftKey_DOWN"),
    ("PAGE_DOWN", "SoftKey_PAGE_DOWN"),
    ("LAST", "SoftKey_LAST"),
]


def build_softkeymask(alloc, out, page_name):
    components = []
    for idx, (_role, key_name) in enumerate(SOFTKEY_SPEC):
        icon_proxy = alloc.next_id("CProxy")
        # no icon object required for structure-only phase - point at nothing yet
        # (ISO-Designer requires a valid child; reuse the shared status-grey rect as
        #  a harmless placeholder icon, swap for a real one later)
        out.append(emit_proxy(icon_proxy, "Icon", GLOBAL_SHARED.status_grey_rect, 0, 0))
        key_id = alloc.next_id("CSoftKey")
        out.append(emit_softkey(key_id, key_name, icon_proxy))
        key_proxy = alloc.next_id("CProxy")
        out.append(emit_proxy(key_proxy, key_name, key_id, 0, 0))
        ptr_id = alloc.next_id("CPointer")
        out.append(emit_object_pointer(ptr_id, f"ObjectPointer_{key_name}", key_proxy))
        components.append(emit_mask_component("CPointer", "Pointer", ptr_id, 0, 560, softkey_designator=idx))

    skm_id = alloc.next_id("CSoftKeyMask")
    jvi_name = f"{page_name}SoftKeyMask.jvi"
    out.append(emit_softkeymask_stub(skm_id, f"{page_name}SoftKeyMask", f".\\{jvi_name}"))
    jvi_content = emit_softkeymask_jvi(skm_id, "".join(components))
    return skm_id, jvi_name, jvi_content


def build_page(alloc, out, shared, page_name, header_row_pairs):
    """header_row_pairs: list of (header_title_or_None, [(col1,col2,col3), ...]) blocks,
    in the order they should appear top to bottom."""
    prefix = page_name  # e.g. "Ausgaenge" / "Eingaenge"

    content_children = []
    top = 0
    row_number = 0
    for header_title, rows in header_row_pairs:
        if header_title is not None:
            content_children.append(build_header_row(alloc, out, shared, top, header_title))
            # Same slot height as a data row (ROW_HEIGHT, not HEADER_H) - the scroll
            # engine assumes one uniform row_height for the whole list; the header's
            # own rectangle is still only HEADER_H tall, just like data rows are only
            # ROW_H tall inside their ROW_HEIGHT slot, leaving the same visual gap.
            top += ROW_HEIGHT
        for col1, col2, col3 in rows:
            row_number += 1
            content_children.append(
                build_data_row(alloc, out, shared, top, col1, col2, col3, prefix, row_number))
            top += ROW_HEIGHT
    content_total_h = top

    list_content_id = alloc.next_id("CGroup")
    out.append(emit_group_with_children(
        list_content_id, f"{prefix}_Scrolling_Content", ROW_W, content_total_h, content_children))

    list_parent_id = alloc.next_id("CGroup")
    lc_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(lc_proxy, f"{prefix}_Scrolling_Content", list_content_id, 0, 0))
    out.append(emit_group_with_children(
        list_parent_id, f"{prefix}_Scrolling_Parent", LIST_PARENT_W, LIST_PARENT_H, [lc_proxy]))

    bar_content_id = alloc.next_id("CGroup")
    thumb_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(thumb_proxy, "Rectangle_BarThumb", shared.bar_thumb_rect, BAR_PARENT_H - BAR_THUMB_H, 0))
    out.append(emit_group_with_children(
        bar_content_id, f"{prefix}_Scrollbar_Content", BAR_PARENT_W, BAR_PARENT_H, [thumb_proxy]))

    bar_parent_id = alloc.next_id("CGroup")
    track_proxy = alloc.next_id("CProxy")
    bc_proxy = alloc.next_id("CProxy")
    out.append(emit_proxy(track_proxy, "Rectangle_BarTrack", shared.bar_track_rect, 0, 0))
    out.append(emit_proxy(bc_proxy, f"{prefix}_Scrollbar_Content", bar_content_id,
                           -(BAR_PARENT_H - BAR_THUMB_H), 0))
    out.append(emit_group_with_children(
        bar_parent_id, f"{prefix}_Scrollbar_Parent", BAR_PARENT_W, BAR_PARENT_H, [track_proxy, bc_proxy]))

    skm_id, skm_jvi_name, skm_jvi_content = build_softkeymask(alloc, out, page_name)

    mask_components = (
        emit_mask_component("CGroup", f"{prefix}_Scrolling_Parent", list_parent_id, 0, 0)
        + emit_mask_component("CGroup", f"{prefix}_Scrollbar_Parent", bar_parent_id, 0, BAR_PARENT_LEFT)
    )
    mask_id = alloc.next_id("CDataMask")
    mask_jvi_name = f"{page_name}Mask.jvi"
    out.append(emit_datamask_stub(mask_id, f"{page_name}Mask", f".\\{mask_jvi_name}"))
    mask_jvi_content = emit_datamask_jvi(mask_id, skm_id, mask_components)

    return {
        "mask_id": mask_id,
        "mask_jvi_name": mask_jvi_name,
        "mask_jvi_content": mask_jvi_content,
        "skm_jvi_name": skm_jvi_name,
        "skm_jvi_content": skm_jvi_content,
        "pos_max": (content_total_h - LIST_PARENT_H) // ROW_HEIGHT,
        "row_count": len(content_children),
    }


GLOBAL_SHARED = None


def main():
    global GLOBAL_SHARED
    with io.open(JOP_PATH, "r", encoding="utf-8", newline="") as f:
        jop_text = f.read()
    assert "\r\n" in jop_text, "expected CRLF line endings in DefaultPool.jop"

    alloc = IdAllocator(jop_text)
    q_groups, i_groups = load_csv_rows()

    out = []
    shared = build_shared_objects(alloc, out)
    GLOBAL_SHARED = shared

    ausgaenge_blocks = []
    for modul in sorted(q_groups):
        entries = sorted(q_groups[modul], key=pin_sort_key)
        rows = [(f"STG{modul} · {e['pin']}", e["funktion"], e["anschluss"]) for e in entries]
        ausgaenge_blocks.append((f"STG{modul}", rows))

    eingaenge_blocks = []
    for modul in sorted(i_groups):
        entries = sorted(i_groups[modul], key=pin_sort_key)
        rows = [(f"STG{modul} · {e['pin']}", e["funktion"], e["anschluss"]) for e in entries]
        eingaenge_blocks.append((f"STG{modul}", rows))
    bosch_rows = [(name, comment, "CAN") for name, comment in BOSCH_FIELDS]
    eingaenge_blocks.append(("Neigungs-/Beschleunigungssensor (Bosch)", bosch_rows))

    ausgaenge_info = build_page(alloc, out, shared, "Ausgaenge", ausgaenge_blocks)
    eingaenge_info = build_page(alloc, out, shared, "Eingaenge", eingaenge_blocks)

    new_objects_text = "".join(out)

    insertion_marker = "\t</Objects>\r\n</JetView-ObjectPool>"
    if insertion_marker in jop_text:
        new_jop_text = jop_text.replace(
            insertion_marker, new_objects_text + insertion_marker, 1)
    else:
        # Fallback: insert right before the last closing </Objects>
        idx = jop_text.rfind("\t</Objects>\r\n")
        assert idx != -1, "could not find </Objects> insertion point in DefaultPool.jop"
        new_jop_text = jop_text[:idx] + new_objects_text + jop_text[idx:]

    with io.open(JOP_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(new_jop_text)

    for info in (ausgaenge_info, eingaenge_info):
        with io.open(os.path.join(JOP_DIR, info["mask_jvi_name"]), "w", encoding="utf-8", newline="") as f:
            f.write(info["mask_jvi_content"])
        with io.open(os.path.join(JOP_DIR, info["skm_jvi_name"]), "w", encoding="utf-8", newline="") as f:
            f.write(info["skm_jvi_content"])

    print(f"Ausgaenge: {ausgaenge_info['row_count']} rows, pos_max={ausgaenge_info['pos_max']}, "
          f"mask ID {ausgaenge_info['mask_id']}")
    print(f"Eingaenge: {eingaenge_info['row_count']} rows, pos_max={eingaenge_info['pos_max']}, "
          f"mask ID {eingaenge_info['mask_id']}")
    print(f"Wrote {len(out)} new objects.")


if __name__ == "__main__":
    main()
