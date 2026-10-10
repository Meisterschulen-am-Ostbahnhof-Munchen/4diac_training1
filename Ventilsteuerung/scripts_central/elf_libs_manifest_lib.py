#!/usr/bin/env python3
"""ELF-Libs-Manifest-Logik - urspruenglich als Python-Portierung von
elf_libs_manifest_lib.sh (Commit 10b540e53, Branch feature/elf-loader) zum
Vergleich entstanden, inzwischen die massgebliche Implementierung: genutzt
von make_libs_manifest.py und make_4diac_training1_deploy.py.

Format/Kanonisierung sind seit 2026-10-09 durch den Firmware-Code
(elf_libs_loader, LOGIBUS_integration_datapanel feature/elf-loader)
festgelegt. Siehe die Git-Historie von elf_libs_manifest_lib.sh (Bash-
Vorgaenger, Branch feature/elf-loader) fuer die ausfuehrliche
Begruendung/Historie jeder einzelnen Tabelle unten - hier nur 1:1
uebernommen, nicht neu hergeleitet.
"""

from __future__ import annotations

import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

VENTILSTEUERUNG_DIR = Path(__file__).resolve().parent.parent

# Architektur je Knoten - UNBESTAETIGTER PLATZHALTER (ausser 192.168.178.55).
NODE_ARCH = {
    "192.168.178.55": "riscv32",
}

# forte_abi: von Hand erhoehte Nummer, wenn sich FORTE-Basisklassen aendern.
FORTE_ABI = 3

# Namensraum-Praefix -> Lib-Name. 1:1 aus elf_libs_manifest_lib.sh
# uebernommen (siehe dort fuer die ausfuehrliche Begruendung der
# Mehrdeutigkeiten/Ausnahmen).
PREFIX_TO_LIB = {
    "BlinkMarine::io": "BlinkMarine",
    "DataPanel::Status": "DataPanel",
    "DataPanel::io": "DataPanel",
    "Funk::io": "Funk",
    "OSCAT::Basic": "OSCAT_Basic",
    "OSCAT::Building": "OSCAT_Building",
    "OSCAT::Network": "OSCAT_Network",
    "OSCAT_adapter": "OSCAT_adapter",
    "adapter::net": "net_adapter",
    "adapter::conversion": "adapter_conversion",
    "adapter::events": "adapter_events",
    "adapter::iec61131": "adapter_iec61131-3",
    "adapter::iec61499": "adapter_events",
    "adapter::selection": "adapter_selection",
    "adapter::signalprocessing": "logiBUS_signalprocessing_adapter",
    "adapter::types": "adapter_types",
    "adapter::utils": "utils_adapter",
    "adapter::Engineering": "adapter",
    "adapter::OverrideK": "adapter",
    "adapter::assembling": "adapter",
    "adapter::bistableElements": "adapter",
    "adapter::bitwiseOperators": "adapter",
    "adapter::booleanOperators": "adapter",
    "adapter::monostableElements": "adapter",
    "adapter::splitting": "adapter",
    "eclipse4diac::convert": "convert",
    "eclipse4diac::rtevents": "rtevents",
    "eclipse4diac::signalprocessing": "signalprocessing",
    "eclipse4diac::storage": "logiBUS_storage",
    "eclipse4diac::utils": "utils",
    "SafeArithmetic::arithmetic": "SafeArithmetic",
    "iec61131::arithmetic": "iec61131-3",
    "iec61131::arrays": "iec61131-3",
    "iec61131::bistableElements": "iec61131-3",
    "iec61131::bitwiseOperators": "iec61131-3",
    "iec61131::booleanOperators": "iec61131-3-bool",
    "iec61131::charString": "iec61131-3",
    "iec61131::comparison": "iec61131-3",
    "iec61131::conversion": "iec61131-3",
    "iec61131::counters": "iec61131-3",
    "iec61131::edgeDetection": "iec61131-3",
    "iec61131::numerical": "iec61131-3",
    "iec61131::selection": "iec61131-3",
    "iec61131::timers": "iec61131-3",
    "isobus::TC": "isobus_TC",
    "isobus::UT": "isobus_UT",
    "isobus::pgn": "isobus_pgn",
    "isobus::tecu": "isobus_tecu",
    "logiBUS::bistableElements": "logiBUS_utils",
    "logiBUS::bosch": "logiBUS_bosch",
    "logiBUS::drives": "logiBUS_utils",
    "logiBUS::esp32": "logiBUS_esp32",
    "logiBUS::io": "logiBUS_io",
    "logiBUS::safety": "logiBUS_safety",
    "logiBUS::signalprocessing": "logiBUS_signalprocessing_adapter",
    "logiBUS::storage": "logiBUS_storage_esp32",
    "logiBUS::utils": "logiBUS_utils",
    "logiBUS::version": "logiBUS_version",
}

# Exakter FBType-Name -> Lib-Name. Hat in resolve_required_libs() IMMER
# Vorrang vor PREFIX_TO_LIB. 1:1 aus elf_libs_manifest_lib.sh uebernommen.
TYPE_NAME_TO_LIB = {
    # adapter::conversion: Default adapter_conversion, Ausnahme logiBUS_utils_adapter
    "AQ_TO_AX": "logiBUS_utils_adapter",
    "AX_TO_AQ": "logiBUS_utils_adapter",
    # adapter::events: Default adapter_events, Ausnahme logiBUS_signalprocessing_adapter (*_D_FF_HYS-Familie)
    "ADI_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "ADI_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AI_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AI_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "ALI_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "ALI_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "ALR_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "ALR_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AR_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AR_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AS_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AS_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AUDI_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AUDI_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AUI_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AUI_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AULI_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AULI_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    "AUS_D_FF_HYS": "logiBUS_signalprocessing_adapter",
    "AUS_D_FF_HYS_TMIN": "logiBUS_signalprocessing_adapter",
    # iec61131::selection: Default iec61131-3, Ausnahme iec61131-3-bool
    "F_MUX_32": "iec61131-3-bool",
    # isobus::UT: Default isobus_UT, Ausnahmen isobus_UT_adapter/isobus_UT_io/
    # isobus_UT_io_adapter/isobus_signalprocessing/isobus_signalprocessing_adapter
    "Q_ActiveMask_AUI": "isobus_UT_adapter",
    "Q_Attribute_AUDI": "isobus_UT_adapter",
    "Q_BackgroundColourAux_AUS": "isobus_UT_adapter",
    "Q_BackgroundColour_AUS": "isobus_UT_adapter",
    "Q_ChildPosition_AI": "isobus_UT_adapter",
    "Q_ExecuteExtendedMacro_AUI": "isobus_UT_adapter",
    "Q_ExecuteMacro_AUI": "isobus_UT_adapter",
    "Q_NumericValueAux_AUDI": "isobus_UT_adapter",
    "Q_NumericValue_AUDI": "isobus_UT_adapter",
    "Q_NumericValue_PHYSA": "isobus_UT_adapter",
    "Q_NumericValue_PHYSA_LREAL": "isobus_UT_adapter",
    "Q_ObjEnableDisable_AB": "isobus_UT_adapter",
    "Q_ObjEnableDisable_AX": "isobus_UT_adapter",
    "Q_ObjHideShow_AB": "isobus_UT_adapter",
    "Q_ObjHideShow_AX": "isobus_UT_adapter",
    "Q_Priority_AUS": "isobus_UT_adapter",
    "Q_SelectColourMap_AUI": "isobus_UT_adapter",
    "Q_SetAudioVolume_AUS": "isobus_UT_adapter",
    "Q_SoftKeyMask_AUI": "isobus_UT_adapter",
    "Q_StringValue_AIS": "isobus_UT_adapter",
    "Attribute_ID": "isobus_UT_io",
    "Aux_IE": "isobus_UT_io",
    "Aux_IX": "isobus_UT_io",
    "Aux_QD": "isobus_UT_io",
    "Aux_QX": "isobus_UT_io",
    "Aux_Val1_IW": "isobus_UT_io",
    "Aux_Val1_QW": "isobus_UT_io",
    "Aux_Val2_IW": "isobus_UT_io",
    "Button_IE": "isobus_UT_io",
    "Button_IX": "isobus_UT_io",
    "NumericValue_ID": "isobus_UT_io",
    "NumericValue_PHYS": "isobus_UT_io",
    "Softkey_IE": "isobus_UT_io",
    "Softkey_IX": "isobus_UT_io",
    "StringValue_IS": "isobus_UT_io",
    "StringValue_IWS": "isobus_UT_io",
    "Attribute_IDA": "isobus_UT_io_adapter",
    "Aux_IXA": "isobus_UT_io_adapter",
    "Aux_QXA": "isobus_UT_io_adapter",
    "Button_IXA": "isobus_UT_io_adapter",
    "NumericValue_IDA": "isobus_UT_io_adapter",
    "NumericValue_PHYSA": "isobus_UT_io_adapter",
    "Softkey_IXA": "isobus_UT_io_adapter",
    "StringValue_AIS": "isobus_UT_io_adapter",
    "StringValue_AIWS": "isobus_UT_io_adapter",
    "BargraphSplitFS": "isobus_signalprocessing",
    "PositionMarkerFS": "isobus_signalprocessing",
    "ReportScrollOffset": "isobus_signalprocessing",
    "ScrollFS": "isobus_signalprocessing",
    "ScrollFS_PHYS_Button": "isobus_signalprocessing",
    "ScrollFS_PHYS_Softkey": "isobus_signalprocessing",
    "BargraphSplitFS_AR": "isobus_signalprocessing_adapter",
    "PositionMarkerFSA": "isobus_signalprocessing_adapter",
    # isobus::tecu: Default isobus_tecu, Ausnahme isobus_tecu_adapter (IA_*)
    "IA_COGSOGRapidUpdate": "isobus_tecu_adapter",
    "IA_FHS": "isobus_tecu_adapter",
    "IA_FPTO": "isobus_tecu_adapter",
    "IA_GBSD": "isobus_tecu_adapter",
    "IA_Lighting": "isobus_tecu_adapter",
    "IA_MSS": "isobus_tecu_adapter",
    "IA_PosDeltaHighPrecRapidUpd": "isobus_tecu_adapter",
    "IA_RHS": "isobus_tecu_adapter",
    "IA_RPTO": "isobus_tecu_adapter",
    "IA_VDS": "isobus_tecu_adapter",
    "IA_VP1": "isobus_tecu_adapter",
    "IA_WBSD": "isobus_tecu_adapter",
    # logiBUS::io: Default logiBUS_io, Ausnahme logiBUS_DI_CAN
    "logiBUS_2_CAN_IX": "logiBUS_DI_CAN",
    "logiBUS_2_CAN_IXA": "logiBUS_DI_CAN",
    # logiBUS::signalprocessing: Default logiBUS_signalprocessing_adapter, Ausnahme logiBUS_signalprocessing (reine Nicht-Adapter-Bausteine)
    "FIELDBUS_BYTE_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_BYTE_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_DWORD_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_DWORD_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_LWORD_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_LWORD_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_QUARTER_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_UDINT_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_UDINT_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_UINT_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_UINT_TO_SIGNAL_COMPOUND_SCALE": "logiBUS_signalprocessing",
    "FIELDBUS_UINT_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_ULINT_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_ULINT_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_USINT_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_USINT_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "FIELDBUS_WORD_TO_SIGNAL": "logiBUS_signalprocessing",
    "FIELDBUS_WORD_TO_SIGNAL_COMPOUND_SCALE": "logiBUS_signalprocessing",
    "FIELDBUS_WORD_TO_SIGNAL_SCALED": "logiBUS_signalprocessing",
    "F_FRACTION_TO_PERCENT": "logiBUS_signalprocessing",
    "F_PERCENT_TO_FRACTION": "logiBUS_signalprocessing",
    "ILOCK_2_E": "logiBUS_signalprocessing",
    "ILOCK_BLOCK": "logiBUS_signalprocessing",
    "ILOCK_BLOCK_PROTECT": "logiBUS_signalprocessing",
    "ILOCK_CONFLICT_TRIP": "logiBUS_signalprocessing",
    "ILOCK_CONFLICT_TRIP_PROTECT": "logiBUS_signalprocessing",
    "ILOCK_SWITCH": "logiBUS_signalprocessing",
    "ILOCK_SWITCH_PROTECT": "logiBUS_signalprocessing",
    "SYS_ONTIME": "logiBUS_signalprocessing",
    # logiBUS::utils: Default logiBUS_utils, Ausnahmen logiBUS_utils_adapter/quarter/logiBUS_schieber
    "AnlagenSequenz_06_ADAPTER": "logiBUS_utils_adapter",
    "BasicOne_AX": "logiBUS_utils_adapter",
    "LinksRechts_AX": "logiBUS_utils_adapter",
    "SchieberControl_AX": "logiBUS_utils_adapter",
    "SchieberVerriegelungComposite": "logiBUS_utils_adapter",
    "sequence_B_08_AX_AX": "logiBUS_utils_adapter",
    "sequence_ET_04_04_AX": "logiBUS_utils_adapter",
    "sequence_ET_04_AX": "logiBUS_utils_adapter",
    "sequence_ET_04_loop_AX": "logiBUS_utils_adapter",
    "sequence_ET_05_AX": "logiBUS_utils_adapter",
    "sequence_ET_05_loop_AX": "logiBUS_utils_adapter",
    "sequence_ET_08_AX": "logiBUS_utils_adapter",
    "sequence_ET_08_loop_AX": "logiBUS_utils_adapter",
    "sequence_E_04_AX": "logiBUS_utils_adapter",
    "sequence_E_04_AX_SR": "logiBUS_utils_adapter",
    "sequence_E_04_loop_AX": "logiBUS_utils_adapter",
    "sequence_E_05_AX": "logiBUS_utils_adapter",
    "sequence_E_05_loop_AX": "logiBUS_utils_adapter",
    "sequence_E_08_AX": "logiBUS_utils_adapter",
    "sequence_E_08_AX_AX": "logiBUS_utils_adapter",
    "sequence_E_08_AX_DM": "logiBUS_utils_adapter",
    "sequence_E_08_loop_AX": "logiBUS_utils_adapter",
    "sequence_Pattern_04_04_loop_AX": "logiBUS_utils_adapter",
    "sequence_Pattern_08_08_loop_AX": "logiBUS_utils_adapter",
    "sequence_T_04_AX": "logiBUS_utils_adapter",
    "sequence_T_04_loop_AX": "logiBUS_utils_adapter",
    "sequence_T_05_AX": "logiBUS_utils_adapter",
    "sequence_T_05_loop_AX": "logiBUS_utils_adapter",
    "sequence_T_08_ADAPTER": "logiBUS_utils_adapter",
    "sequence_T_08_AX": "logiBUS_utils_adapter",
    "sequence_T_08_loop_AX": "logiBUS_utils_adapter",
    "BOOLS_TO_QUARTERS": "quarter",
    "BOOL_TO_QUARTER": "quarter",
    "E_SREN": "quarter",
    "QUARTERS_TO_BOOLS": "quarter",
    "QUARTER_TO_BOOL": "quarter",
    "QUARTER_TO_E": "quarter",
    "QUARTER_TO_STR_MEASURED": "quarter",
    "QUARTER_TO_STR_STATUS": "quarter",
    "SchieberControl": "logiBUS_schieber",
    "SchieberVerriegelung": "logiBUS_schieber",
}

# Lib-Version, die aktuell als ELF gebaut/erwartet wird. 1:1 aus
# elf_libs_manifest_lib.sh uebernommen. logiBUS_stations/core/events/net/
# system bewusst NICHT eingetragen (kein eigenes ELF, siehe Bash-Original).
LIB_VERSIONS = {
    "BlinkMarine": "3.0.0",
    "DataPanel": "3.0.0",
    "Funk": "3.0.0",
    "OSCAT_Basic": "0.1.0",
    "OSCAT_Building": "0.1.0",
    "OSCAT_Network": "0.1.0",
    "OSCAT_adapter": "3.0.0",
    "SafeArithmetic": "3.0.0",
    "adapter": "3.0.0",
    "adapter_conversion": "3.0.0",
    "adapter_events": "3.0.0",
    "adapter_iec61131-3": "3.0.0",
    "adapter_selection": "3.0.0",
    "adapter_types": "3.0.0",
    "convert": "3.0.0",
    "iec61131-3": "3.0.0",
    "iec61131-3-bool": "3.0.0",
    "isobus_TC": "3.0.0",
    "isobus_UT": "3.0.0",
    "isobus_UT_adapter": "3.0.0",
    "isobus_UT_io": "3.0.0",
    "isobus_UT_io_adapter": "3.0.0",
    "isobus_pgn": "3.0.0",
    "isobus_signalprocessing": "3.0.0",
    "isobus_signalprocessing_adapter": "3.0.0",
    "isobus_tecu": "3.0.0",
    "isobus_tecu_adapter": "3.0.0",
    "logiBUS_DI_CAN": "3.0.0",
    "logiBUS_bosch": "3.0.0",
    "logiBUS_esp32": "3.0.0",
    "logiBUS_io": "3.0.0",
    "logiBUS_safety": "3.0.0",
    "logiBUS_schieber": "3.0.0",
    "logiBUS_signalprocessing": "3.0.0",
    "logiBUS_signalprocessing_adapter": "3.0.0",
    "logiBUS_storage": "3.0.0",
    "logiBUS_storage_esp32": "3.0.0",
    "logiBUS_utils": "3.0.0",
    "logiBUS_utils_adapter": "3.0.0",
    "logiBUS_version": "3.0.0",
    "net_adapter": "3.0.0",
    "quarter": "3.0.0",
    "rtevents": "3.0.0",
    "signalprocessing": "3.0.0",
    "utils": "3.0.0",
    "utils_adapter": "3.0.0",
}

# Lib-Ordnername unter 4diacIDE-workspace/.lib/ (nicht einheitlich). 1:1 aus
# elf_libs_manifest_lib.sh uebernommen.
LIB_DIR_NAME = {
    "BlinkMarine": "BlinkMarine-3.0.0",
    "DataPanel": "DataPanel-3.0.0",
    "Funk": "Funk-3.0.0",
    "OSCAT_Basic": "OSCAT_Basic-0.1.0",
    "OSCAT_Building": "OSCAT_Building-0.1.0",
    "OSCAT_Network": "OSCAT_Network-0.1.0",
    "OSCAT_adapter": "OSCAT_adapter-3.0.0",
    "SafeArithmetic": "SafeArithmetic-3.0.0",
    "adapter": "adapter-3.0.0",
    "adapter_conversion": "adapter_conversion-3.0.0",
    "adapter_events": "adapter_events-3.0.0",
    "adapter_iec61131-3": "adapter_iec61131-3-3.0.0",
    "adapter_selection": "adapter_selection-3.0.0",
    "adapter_types": "adapter_types-3.0.0",
    "convert": "convert-3.0.0",
    "iec61131-3": "iec61131-3-3.0.0",
    "iec61131-3-bool": "iec61131-3-bool-3.0.0",
    "isobus_TC": "isobus_TC-3.0.0",
    "isobus_UT": "isobus_UT-3.0.0",
    "isobus_UT_adapter": "isobus_UT_adapter-3.0.0",
    "isobus_UT_io": "isobus_UT_io-3.0.0",
    "isobus_UT_io_adapter": "isobus_UT_io_adapter-3.0.0",
    "isobus_pgn": "isobus_pgn-3.0.0",
    "isobus_signalprocessing": "isobus_signalprocessing-3.0.0",
    "isobus_signalprocessing_adapter": "isobus_signalprocessing_adapter-3.0.0",
    "isobus_tecu": "isobus_tecu-3.0.0",
    "isobus_tecu_adapter": "isobus_tecu_adapter-3.0.0",
    "logiBUS_DI_CAN": "logiBUS_DI_CAN-3.0.0",
    "logiBUS_bosch": "logiBUS_bosch-3.0.0",
    "logiBUS_esp32": "logiBUS_esp32-3.0.0",
    "logiBUS_io": "logiBUS_io-3.0.0",
    "logiBUS_safety": "logiBUS_safety-3.0.0",
    "logiBUS_schieber": "logiBUS_schieber-3.0.0",
    "logiBUS_signalprocessing": "logiBUS_signalprocessing-3.0.0",
    "logiBUS_signalprocessing_adapter": "logiBUS_signalprocessing_adapter-3.0.0",
    "logiBUS_storage": "logiBUS_storage-3.0.0",
    "logiBUS_storage_esp32": "logiBUS_storage_esp32-3.0.0",
    "logiBUS_utils": "logiBUS_utils-3.0.0",
    "logiBUS_utils_adapter": "logiBUS_utils_adapter-3.0.0",
    "logiBUS_version": "logiBUS_version-3.0.0",
    "net_adapter": "net_adapter-3.0.0",
    "quarter": "quarter-3.0.0",
    "rtevents": "rtevents-3.0.0",
    "signalprocessing": "signalprocessing-3.0.0",
    "utils": "utils-3.0.0",
    "utils_adapter": "utils_adapter-3.0.0",
}

ELF_DIR = "elf-libs"

# Firmware-Limits (siehe elf_libs_manifest_lib.sh fuer Historie/Begruendung).
MAX_LIBS = 16
MAX_LIBS_PLUS_FILES = 64
MAX_REQ = 8
MAX_MANIFEST_BYTES = 65536

_TYPE_RE = re.compile(r'Type="([A-Za-z0-9_]+(?:::[A-Za-z0-9_]+)+)"')
_REQUIRED_TAG = "Required"
_PRODUCT_TAG = "Product"
_VERSIONINFO_TAG = "VersionInfo"


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_of_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _manifest_mf_path(lib: str) -> Path:
    dir_name = LIB_DIR_NAME.get(lib, lib)
    return VENTILSTEUERUNG_DIR / "4diacIDE-workspace" / ".lib" / dir_name / "MANIFEST.MF"


def mf_version_of(lib: str) -> str:
    """Liest Product/VersionInfo/@Version aus der echten MANIFEST.MF.
    Leer, wenn die Datei fehlt oder nicht geparst werden kann."""
    mf = _manifest_mf_path(lib)
    if not mf.is_file():
        return ""
    try:
        root = ET.parse(mf).getroot()
    except ET.ParseError:
        return ""
    product = root.find(_PRODUCT_TAG)
    if product is None:
        return ""
    version_info = product.find(_VERSIONINFO_TAG)
    if version_info is None:
        return ""
    return version_info.get("Version", "")


_lib_requires_cache: dict[str, list[tuple[str, str]]] = {}


def lib_requires_of(lib: str) -> list[tuple[str, str]]:
    """Liest die requires-Liste einer Lib ("Name", "Range") direkt aus deren
    MANIFEST.MF - einzige Quelle, keine von Hand gepflegte Tabelle (siehe
    elf_libs_manifest_lib.sh: genau das war der Grund fuer einen echten
    Geraete-Fehler, "Can't find common ...FORTE_F_NOT_BOOL...", weil die
    Bash-Tabelle LIB_REQUIRES["adapter"] nicht synchron gehalten wurde).
    Nur Required-Eintraege, zu denen es ein LIB_VERSIONS-Element (= gebautes
    ELF) gibt. Range ist "^Major.Minor" der in MANIFEST.MF deklarierten
    Version. Ergebnis wird pro Lib gecacht."""
    if lib in _lib_requires_cache:
        return _lib_requires_cache[lib]

    result: list[tuple[str, str]] = []
    mf = _manifest_mf_path(lib)
    if mf.is_file():
        try:
            root = ET.parse(mf).getroot()
        except ET.ParseError:
            root = None
        if root is not None:
            deps = root.find("Dependencies")
            if deps is not None:
                for req in deps.findall(_REQUIRED_TAG):
                    name = req.get("SymbolicName", "")
                    ver = req.get("Version", "")
                    if name not in LIB_VERSIONS:
                        continue
                    parts = ver.split(".")
                    major = parts[0] if parts else ""
                    minor = parts[1] if len(parts) > 1 else "0"
                    result.append((name, f"^{major}.{minor}"))

    if len(result) > MAX_REQ:
        print(
            f"  WARNUNG: Lib '{lib}' hat {len(result)} requires, "
            f"Firmware erlaubt max. {MAX_REQ} (MAX_REQ).",
        )

    _lib_requires_cache[lib] = result
    return result


def resolve_required_libs(fboot_path: Path) -> list[str]:
    """Liest die benoetigten Lib-Namen aus einem .fboot: zu jedem Type="..."
    zuerst den letzten Segment (den eigentlichen FBType-Namen) exakt gegen
    TYPE_NAME_TO_LIB pruefen (IMMER Vorrang), sonst den Zwei-Segment-
    Namensraum-Key gegen PREFIX_TO_LIB, sonst den Einzelsegment-Key als
    Fallback, dann transitiv ueber lib_requires_of() erweitern (BFS,
    Einfuegereihenfolge wie im Bash-Original)."""
    content = fboot_path.read_text(encoding="utf-8", errors="replace")
    types = sorted(set(_TYPE_RE.findall(content)))

    seen: set[str] = set()
    queue: list[str] = []

    def add(name: str) -> None:
        if name and name not in seen:
            seen.add(name)
            queue.append(name)

    for full in types:
        name = full.rsplit("::", 1)[-1]
        lib = TYPE_NAME_TO_LIB.get(name)
        if lib is None:
            segs = full.split("::")
            if len(segs) >= 3:
                # seg1::seg2 (Zwei-Segment-Namensraum-Key)
                lib = PREFIX_TO_LIB.get(f"{segs[0]}::{segs[1]}")
            if lib is None:
                lib = PREFIX_TO_LIB.get(segs[0])
        if lib:
            add(lib)

    i = 0
    while i < len(queue):
        lib = queue[i]
        i += 1
        for name, _range in lib_requires_of(lib):
            add(name)

    return queue


def resolve_elf_path(lib: str, version: str, arch: str) -> Optional[Path]:
    """Findet den lokalen Pfad eines Lib-ELFs: ELF_DIR flach, sonst
    Repo-Pfad 4diacIDE-workspace/.lib/<LibVerzeichnis>/elf/<arch>/
    <Name>-<Version>-<arch>.elf."""
    fname = f"{lib}-{version}-{arch}.elf"
    flat = VENTILSTEUERUNG_DIR / ELF_DIR / fname
    if flat.is_file():
        return flat
    dir_name = LIB_DIR_NAME.get(lib, lib)
    repo_path = VENTILSTEUERUNG_DIR / "4diacIDE-workspace" / ".lib" / dir_name / "elf" / arch / fname
    if repo_path.is_file():
        return repo_path
    return None


class ManifestResult:
    def __init__(self, ok: bool, elf_paths: Optional[list[Path]] = None):
        self.ok = ok
        self.elf_paths = elf_paths or []


def build_libs_manifest(arch: str, files: list[Path], out_path: Path, libs: list[str]) -> ManifestResult:
    """Baut <programm>.libs.json. Analog zu build_libs_manifest() in
    elf_libs_manifest_lib.sh - gleiche Firmware-Limits, gleiche
    Abbruchbedingungen, gleiches JSON-Format, gleiche manifest_sha256-
    Berechnung (sha256 ueber die nach Dateiname sortierten
    "<dateiname>:<sha256>"-Zeilen aller libs+files, NICHT ueber den
    JSON-Text selbst - muss exakt cmp_hashed() in elf_libs_loader.c
    entsprechen)."""
    if len(libs) > MAX_LIBS:
        print(f"  WARNUNG: {len(libs)} Libs benoetigt, Firmware erlaubt max. {MAX_LIBS} - uebersprungen.")
        return ManifestResult(False)
    if len(libs) + len(files) > MAX_LIBS_PLUS_FILES:
        print(
            f"  WARNUNG: {len(libs)} Libs + {len(files)} Dateien > {MAX_LIBS_PLUS_FILES} "
            "Eintraege (Firmware-Limit) - uebersprungen.",
        )
        return ManifestResult(False)

    for lib in libs:
        req_count = len(lib_requires_of(lib))
        if req_count > MAX_REQ:
            print(
                f"  WARNUNG: Lib '{lib}' hat {req_count} requires, Firmware erlaubt "
                f"max. {MAX_REQ} (MAX_REQ) - uebersprungen.",
            )
            return ManifestResult(False)

    elf_path_of: dict[str, Path] = {}
    for lib in libs:
        version = LIB_VERSIONS.get(lib, "")
        if not version:
            print(f"  WARNUNG: Keine Version fuer Lib '{lib}' in LIB_VERSIONS hinterlegt - uebersprungen.")
            return ManifestResult(False)
        mf_ver = mf_version_of(lib)
        if mf_ver and mf_ver != version:
            print(
                f"  WARNUNG: LIB_VERSIONS[{lib}]={version} stimmt nicht mit MANIFEST.MF "
                f"({mf_ver}) ueberein - LIB_VERSIONS aktualisieren. Uebersprungen.",
            )
            return ManifestResult(False)
        elf_path = resolve_elf_path(lib, version, arch)
        if elf_path is None:
            dir_name = LIB_DIR_NAME.get(lib, lib)
            print(
                f"  Hinweis: ELF fehlt lokal ({lib}-{version}-{arch}.elf, weder in "
                f"{ELF_DIR}/ noch unter 4diacIDE-workspace/.lib/{dir_name}/elf/{arch}/) "
                "- uebersprungen.",
            )
            return ManifestResult(False)
        elf_path_of[lib] = elf_path

    canon_lines: list[str] = []
    lib_json_entries = []
    for lib in libs:
        elf_path = elf_path_of[lib]
        version = LIB_VERSIONS[lib]
        fname = elf_path.name
        size = elf_path.stat().st_size
        sha = sha256_of(elf_path)
        canon_lines.append(f"{fname}:{sha}")
        requires = [{"name": n, "range": r} for n, r in lib_requires_of(lib)]
        lib_json_entries.append(
            {
                "name": lib,
                "version": version,
                "file": fname,
                "size": size,
                "sha256": sha,
                "requires": requires,
            },
        )

    file_json_entries = []
    for f in files:
        fname = f.name
        size = f.stat().st_size
        sha = sha256_of(f)
        canon_lines.append(f"{fname}:{sha}")
        file_json_entries.append({"file": fname, "size": size, "sha256": sha})

    names = [line.split(":", 1)[0] for line in canon_lines]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        print(f"  WARNUNG: Doppelte Dateinamen zwischen libs[] und files[] ({' '.join(dup)}) - uebersprungen.")
        return ManifestResult(False)

    # Sortierung nach Dateiname (vor dem ersten ":"), reine Byte-/ASCII-
    # Ordnung (= LC_ALL=C sort -t: -k1,1 im Bash-Original) - muss exakt
    # cmp_hashed() (elf_libs_loader.c, sortiert nur ueber .name) entsprechen.
    sorted_lines = sorted(canon_lines, key=lambda line: line.split(":", 1)[0])
    manifest_sha = sha256_of_text("\n".join(sorted_lines) + "\n")

    manifest = {
        "format": 1,
        "forte_abi": FORTE_ABI,
        "arch": arch,
        "libs": lib_json_entries,
        "files": file_json_entries,
        "manifest_sha256": manifest_sha,
        "signature": None,
    }

    text = json.dumps(manifest, indent=2) + "\n"
    # LF-Zeilenenden erzwingen (newline="") statt der Windows-Textmode-
    # Standarduebersetzung zu CRLF - gleicher Grund wie beim Bash-Original.
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)

    manifest_size = out_path.stat().st_size
    if manifest_size > MAX_MANIFEST_BYTES:
        print(f"  WARNUNG: Manifest {manifest_size} Bytes > 64 KB (Firmware-Limit) - uebersprungen.")
        out_path.unlink(missing_ok=True)
        return ManifestResult(False)

    return ManifestResult(True, [elf_path_of[lib] for lib in libs])
